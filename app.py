from flask import Flask, jsonify, request, url_for, flash, render_template
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
from flask_migrate import Migrate
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from werkzeug.urls import url_parse
from werkzeug.utils import redirect

from blacklist import revoked_store

from db import db
from forms.admin import AdminLoginForm
from ma import ma

from models.admin import AdminUserModel
from models.user import UserModel
from models.data import ClipDataModel
from models.restaurant import RestaurantModel, ClipModel, TagModel
from models.relevance import RelevanceModel
from models.confirmation import ConfirmationModel

from resources.user import (
    UserRegister,
    User,
    UserLogin,
    TokenRefresh,
    UserLogout,
    UserDelete,
    AdminLogin,
    AdminRevokeToken,
    AdminTokenRefresh,
)
from resources.confirmation import Confirmation, ConfirmationByUser
from resources.admin import AdminHome, AdminRestaurant, AddTag, UploadClip, AdminAddRestaurant
from resources.restaurant import Restaurant, AddRestaurant, Restaurants
from resources.relevance import UpdateRelevance

app = Flask(__name__)

migrate = Migrate(app, db)

api = Api(app)

jwt = JWTManager(app)

admin_login = LoginManager(app)
admin_login.login_view = 'admin_login'

# ADMIN STUFF HERE FOR EASE.
class ProtectedAdminHomeView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('admin_login', next=request.url))

    @expose('/')
    def index(self):
        return self.render('/admin/index.html')


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('admin_login', next=request.url))


@admin_login.user_loader
def load_user(id):
    return AdminUserModel.query.get(int(id))


@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = AdminLoginForm()
    if form.validate_on_submit():
        user = AdminUserModel.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect((url_for('admin_login')))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('admin-login.html', title='Log In', form=form)


@app.route('/admin-logout')
def logout():
    logout_user()
    return redirect("https://munchy.fun")

admin = Admin(app, name='Munchy', template_mode='bootstrap3', index_view=ProtectedAdminHomeView(url='/admin'))
admin.add_view(AdminView(UserModel, db.session))
admin.add_view(AdminView(ClipDataModel, db.session))
admin.add_view(AdminView(RestaurantModel, db.session))
admin.add_view(AdminView(ClipModel, db.session))
admin.add_view(AdminView(TagModel, db.session))
admin.add_view(AdminView(RelevanceModel, db.session))
admin.add_view(AdminView(ConfirmationModel, db.session))


# List of user_id's for admin users.
ADMIN_IDENTITIES = [1, ]

EXPIRED_TOKEN = "The token has expired."
INVALID_TOKEN = "The token is invalid."
UNAUTHORIZED = "An access token is required."
NEEDS_FRESH_TOKEN = "A fresh token is required."
REVOKED_TOKEN = "The token has been revoked."


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity in ADMIN_IDENTITIES:
        return {"is_admin": True}
    return {"is_admin": False}


@jwt.token_in_blacklist_loader
def check_if_token_is_revoked(decrypted_token):
    jti = decrypted_token["jti"]
    entry = revoked_store.get(jti)
    if entry is None:
        return True
    return entry == "true"


# Called when an expired token is used.
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        "description": EXPIRED_TOKEN,
        "error": "token_expired"
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        "description": INVALID_TOKEN,
        "error": "invalid_token"
    }), 401


@jwt.unauthorized_loader
def unauthorized_callback(error):
    return jsonify({
        "description": UNAUTHORIZED,
        "error": "authorization_required"
    }), 401


@jwt.needs_fresh_token_loader
def needs_fresh_token_callback():
    return jsonify({
        "description": NEEDS_FRESH_TOKEN,
        "error": "fresh_token_required"
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": REVOKED_TOKEN,
        "error": "revoked_token"
    }), 401


api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserDelete, "/user-delete")
api.add_resource(TokenRefresh, "/token-refresh")
api.add_resource(Confirmation, "/user-confirmation/<string:confirmation_id>")

#api.add_resource(AdminHome, "/admin2")
#api.add_resource(AdminLogin, "/admin/login")
#api.add_resource(AdminTokenRefresh, "/admin/token-refresh")
#api.add_resource(AdminRevokeToken, "/admin/token-revoke")

#api.add_resource(AddTag, "/admin/add-tag")
#api.add_resource(AdminAddRestaurant, "/admin/add-restaurant")

api.add_resource(UploadClip, "/upload")

# Restaurant resources.
api.add_resource(Restaurant, "/restaurant/<int:restaurant_id>")
api.add_resource(AddRestaurant, "/add-restaurant")
api.add_resource(Restaurants, "/restaurants")

# Relevance
api.add_resource(UpdateRelevance, "/update-relevance")

# Possibly just change to resend confirmation. Get rid of get method for testing.
api.add_resource(ConfirmationByUser, "/confirmation/user/<int:user_id>")


# Admin
app.config.from_object("config.DevelopmentConfig")
db.init_app(app)
ma.init_app(app)

# Registers the db and marshmallow with the app .
if __name__ == "__main__":
    app.config.from_object("config.DevelopmentConfig")  # Can change this to production or testing.
    app.run(port=5000, debug=True)
