import os

from typing import List
from requests import post

LOAD_API_KEY_FAILED = "Failed to load Mailgun API key."
LOAD_DOMAIN_FAILED = "Failed to load Mailgun domain."
SEND_EMAIL_FAILED = "Error sending confirmation email, user registration failed."


class MailgunException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class Mailgun:
    MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")
    MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")

    FROM_TITLE = "Boomerang Refunds"
    FROM_EMAIL = "mailgun@sandboxfed5b8a55a914ec393f8065fc7b34b04.mailgun.org"

    @classmethod
    def send_email(cls, email: List[str], subject: str, text: str, html: str):
        if cls.MAILGUN_API_KEY is None:
            raise MailgunException(LOAD_API_KEY_FAILED)

        if cls.MAILGUN_DOMAIN is None:
            raise MailgunException(LOAD_DOMAIN_FAILED)

        response = post(
            "https://api.mailgun.net/v3/{}/messages".format(cls.MAILGUN_DOMAIN),
            auth=("api", cls.MAILGUN_API_KEY),
            data={"from": "{} <{}>".format(cls.FROM_TITLE, cls.FROM_EMAIL),
                  "to": email,
                  "subject": subject,
                  "text": text,
                  "html": html,
                  },
        )
        print(response.status_code)
        if response.status_code != 200:
            raise MailgunException(SEND_EMAIL_FAILED)

        return response