import json

import requests
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from werkzeug.utils import redirect

from libs.gmail import Gmail


# NEED TO ADD JWT REQUIRED TO SOME OF THESE AT LEAST.

class GmailLink(Resource):
    @classmethod
    def get(cls):
        # Find out what URL to hit for Google login
        google_provider_cfg = Gmail.get_google_provider_cfg()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        # Use library to construct the request for Google login and provide
        # scopes that let you retrieve user's profile from Google
        request_uri = Gmail.googleClient.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=request.base_url + "/callback",
            scope=["openid", "email", "profile"],
        )
        print("this is the request_uri: {}".format(request_uri))
        return redirect(request_uri)
        #return {"request_uri": request_uri}, 200


class GmailLinkCallback(Resource):
    @classmethod
    def get(cls):
        # Get authorization code from Google
        code = request.args.get("code")

        # Find out what URL to hit to get tokens that allow you to ask for
        # things on behalf of a user
        google_provider_cfg = Gmail.get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]

        # Prepare and send a request to get the tokens.
        token_url, headers, body = Gmail.googleClient.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code
        )

        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(Gmail.GOOGLE_CLIENT_ID, Gmail.GOOGLE_CLIENT_SECRET),
        )

        # Parse the tokens.
        Gmail.googleClient.parse_request_body_response(json.dumps(token_response.json()))
        print(token_response.text)

        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = Gmail.googleClient.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)

        # Check gmail user is verified.
        if userinfo_response.json().get("email_verified"):
            print(userinfo_response.json())
            unique_id = userinfo_response.json()["sub"]
            users_email = userinfo_response.json()["email"]
            picture = userinfo_response.json()["picture"]
            users_name = userinfo_response.json()["given_name"]
        else:
            return "User email not available or not verified by Google.", 400

        print(users_email)
        print(users_name)
        print(unique_id)


class IMAPLogin(Resource):
    @classmethod
    def get(cls):
        user_json = request.get_json()

        email = user_json['email']
        password = user_json['password']
        server = user_json['server']

        #