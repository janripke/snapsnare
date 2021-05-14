import os
import smtplib
import snapsnare
from pathlib import Path
from snapsnare.system import utils
import json

# with open('/home/kozzy/.snapsnare/gmail-ds.json') as f:
#     credentials = json.load(f)

# print(f.)


def send_email(credentials, recipients, message):
    account = credentials['account']
    password = credentials['password']

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    server.login(account, password)
    server.sendmail(account, recipients, message)


properties = {
    'current.dir': os.path.abspath(os.getcwd()),
    'package.dir': os.path.dirname(snapsnare.__file__),
    'home.dir': str(Path.home()),
    'app.name': 'snapsnare'
}

settings = utils.load_json(properties, 'snapsnare.json')
credentials = settings['gmail']

send_email(credentials, 'janripke@gmail.com', "hello world")
