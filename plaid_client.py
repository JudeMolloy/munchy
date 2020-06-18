import os
import plaid

from flask import render_template
from flask import request
from flask import jsonify

PLAID_CLIENT_ID = os.environ.get("PLAID_CLIENT_ID")
PLAID_SECRET = os.environ.get("PLAID_SECRET")
PLAID_PUBLIC_KEY = os.environ.get("PLAID_PUBLIC_KEY")
PLAID_ENV = os.environ.get("PLAID_ENV")


client = plaid.Client(PLAID_CLIENT_ID,
                             PLAID_SECRET,
                             PLAID_PUBLIC_KEY,
                             PLAID_ENV,
                             )
