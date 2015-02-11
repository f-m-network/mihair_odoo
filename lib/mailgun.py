# -*- coding: UTF-8 -*-
#
# Juan Hernandez, 2014
#
# mailgun/email functions
#
import requests
import types
import os

# Mailgun
MG_FROM_EMAIL = os.environ.get('MG_FROM_EMAIL')
MG_FROM_NAME = os.environ.get('MG_FROM_NAME')
MG_HOST_URL = os.environ.get('MG_HOST_URL')
MG_API_KEY = os.environ.get('MG_API_KEY')
MG_SMTP_USER = os.environ.get('MG_SMTP_USER')
MG_SMTP_PASSWORD = os.environ.get('MG_SMTP_PASSWORD')


def send_html_message(email_list, subject, html_message,
                      tag='New PO', tracking=True, files=[],
                      file_open=True):
    if files:
        if isinstance(files, types.StringType):
            files = [files]
        if file_open:
            files = [("attachment", open(f)) for f in files]
        else:
            files = [("attachment", f) for f in files]
    return requests.post(
        "https://api.mailgun.net/v2/{}/messages".format(MG_HOST_URL),
        auth=("api", MG_API_KEY),
        data={"from": '{} <{}>'.format(MG_FROM_NAME, MG_FROM_EMAIL),
              "to": email_list,
              "subject": subject,
              "html": html_message,
              "o:tag": tag,
              "o:tracking": tracking},
        files=files,
    )


