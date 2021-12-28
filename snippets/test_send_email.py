import os
import smtplib
import snapsnare
from pathlib import Path
from snapsnare.system import utils
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

# with open('/home/kozzy/.snapsnare/gmail-ds.json') as f:
#     credentials = json.load(f)

# print(f.)


def send_email(credentials, recipients, subject, content):
    account = credentials['account']
    password = credentials['password']
    smtp_host = credentials['host']
    smtp_port = credentials['port']

    message = MIMEMultipart()
    message['From'] = account
    message['To'] = recipients
    message['Subject'] = subject
    message.attach(MIMEText(content, 'html'))

    server = smtplib.SMTP_SSL(smtp_host, smtp_port)
    server.ehlo()
    server.login(account, password)
    server.sendmail(account, recipients, message.as_string())
    server.close()


properties = {
    'current.dir': os.path.abspath(os.getcwd()),
    'package.dir': os.path.dirname(snapsnare.__file__),
    'home.dir': str(Path.home()),
    'app.name': 'snapsnare'
}

settings = utils.load_json(properties, 'snapsnare.json')
credentials = settings['gmail']
snapsnare = settings['snapsnare']

uuid = "80c1fbd2-0c45-49da-9b24-b8666cd118f8"
host = snapsnare['host']
content = "<img src=http://snapsnare.org/static/snapsnare.png><br>Er is een account voor je aangemaakt.<br> Ga naar <a href=http://{host}/activate?uuid={uuid}>http://{host}/activate?uuid={uuid}</a> om je account te activeren."
content = content.replace("{host}", host)
content = content.replace("{uuid}", uuid)

send_email(credentials, 'janripke@gmail.com', "activate your account", content)
