from db import db


class ClipDataModel(db.Model):
    __tablename__ = "clip_data"

    id = db.Column(db.Integer, primary_key=True)
    views = db.Column(db.Integer, default=0)
    liked = db.Column(db.Boolean, default=False)
    share_clicks = db.Column(db.Integer, default=0)
    map_clicks = db.Column(db.Integer, default=0)

    # Order clicks.
    deliveroo_clicks = db.Column(db.Integer, default=0)
    uber_eats_clicks = db.Column(db.Integer, default=0)
    just_eat_clicks = db.Column(db.Integer, default=0)

    # Link to UserModel.
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("UserModel")

    # Link to ClipModel.
    clip_id = db.Column(db.Integer, db.ForeignKey("clips.id"), nullable=False)
    clip = db.relationship("ClipModel")

    def increment_views(self):
        self.views += 1

    def increment_share_clicks(self):
        self.share_clicks += 1

    def increment_map_clicks(self):
        self.map_clicks += 1

    def increment_swipe_engagements(self):
        self.swipe_engagements += 1

    def increment_deliveroo_clicks(self):
        self.deliveroo_clicks += 1

    def increment_uber_eats_clicks(self):
        self.uber_eats_clicks += 1

    def increment_just_eat_clicks(self):
        self.just_eat_clicks += 1

    def order_clicks(self):
        order_clicks = self.deliveroo_clicks + self.uber_eats_clicks + self.just_eat_click
        return order_clicks

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
