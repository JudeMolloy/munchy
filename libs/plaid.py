import datetime
import traceback

import plaid
from flask import jsonify

from schemas.transaction import TransactionSchema
from plaid_client import client

transaction_schema = TransactionSchema()

TRANSACTIONS_FAILED = "Failed to fetch all transactions."


def fetch_transactions(item):
    # Pull transactions for the last 45 days
    start_date = '{:%Y-%m-%d}'.format(datetime.datetime.now() + datetime.timedelta(-45))
    end_date = '{:%Y-%m-%d}'.format(datetime.datetime.now())
    try:
        transactions_response = client.Transactions.get(item.access_token, start_date, end_date)
        transactions = transactions_response['transactions']

        item_id_json = {"item_id": item.id, }

        for transaction in transactions:
            print("Transaction response is: {}".format(transaction))
            transaction_object = transaction_schema.load(item_id_json, partial=True)
            print(transaction_object)
            transaction_object.save_to_db()
            print(transaction_object)
            transaction_schema.load(transaction, instance=transaction_object, partial=True)
            print(transaction_object)
            transaction_object.save_to_db()
            print(transaction_object)

        print(transactions_response)

    except plaid.errors.PlaidError as e:
        return jsonify({'error': {'display_message': e.display_message, 'error_code': e.code, 'error_type': e.type}})
    except:
        traceback.print_exc()
        return {"message": TRANSACTIONS_FAILED}, 500
