from __future__ import print_function

import base64
import os

from email.message import EmailMessage
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from gc_google_services_api.auth import Auth

AUTHENTICATION_EMAIL = os.getenv('AUTHENTICATION_EMAIL', '')

SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
]


class Gmail:
    def __init__(self, subject_email) -> None:
        self.credentials = Auth(SCOPES, subject_email).get_credentials()
        self.service = build('gmail', 'v1', credentials=self.credentials)

    def send_email(self, email_message, email_subject, to=[]):
        try:
            message = EmailMessage()

            message.set_content(email_message)

            message['to'] = to
            message['from'] = AUTHENTICATION_EMAIL
            message['subject'] = email_subject

            # encoded message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
                .decode()

            create_message = {
                'raw': encoded_message
            }
            send_message = (self.service.users().messages().send
                            (userId='me', body=create_message).execute())
            print(F'Message Id: {send_message["id"]}')
        except HttpError as error:
            print(F'An error occurred: {error}')
            send_message = None

        return send_message
