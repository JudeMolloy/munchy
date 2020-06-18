import traceback
import json

from flask import request, make_response, render_template, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required, get_raw_jwt
from flask_restful import Resource

from libs.plaid import fetch_transactions
from models.item import ItemModel
from models.user import UserModel
from schemas.item import ItemSchema
from plaid_client import client

item_schema = ItemSchema()

ITEM_LINK_SUCCESSFULLY = "Bank account successfully linked."
ITEM_LINK_FAILED = "Failed to link bank account."
ITEM_FETCH_FAILED = "Failed to get items for current user."


class Link(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        current_user_id = get_jwt_identity()
        current_user = UserModel.find_by_id(current_user_id)

        plaid_public_token = request.form['public_token']
        print(plaid_public_token)
        exchange_response = client.Item.public_token.exchange(plaid_public_token)

        plaid_access_token = exchange_response['access_token']
        plaid_item_id = exchange_response['item_id']

        # Request.form is where this data comes from not the exchange response.
        link_session_id = request.form['link_session_id']
        institution_id = request.form['institution_id']
        institution_name = request.form['institution_name']
        print('access token: ' + exchange_response['access_token'])
        print('item ID: ' + exchange_response['item_id'])

        json_data = {"access_token": plaid_access_token,
                               "link_session_id": link_session_id,
                               "institution_id": institution_id,
                               "institution_name": institution_name,
                               "user_id": current_user.id,}

        print(json_data)

        # This won't work because request.form isn't json
        # Need to convert to json in front end or convert in this method.

        # Gets to this part currently. Need to sort that request.form isn't json
        # Possibly need to fix the item init with current user above.
        try:
            item = item_schema.load(json_data, partial=True)
            item.save_to_db()
            fetch_transactions(item=item)
            print("worked")
            return {"message": ITEM_LINK_SUCCESSFULLY}, 201
        except:
            traceback.print_exc()
            print("failed")
            return {"message": ITEM_LINK_FAILED}, 500


class LinkTest(Resource):
    @classmethod
    def get(cls):
        jwt = get_raw_jwt()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('link.html', jwt=jwt), 200, headers)


class Item(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        current_user_id = get_jwt_identity()
        current_user = UserModel.find_by_id(current_user_id)

        try:
            return (
                {
                    "items": [
                        item_schema.dump(each)
                        for each in current_user.get_items
                    ]
                },
                200
            )
        except:
            return {"message": ITEM_FETCH_FAILED}, 500
