import os
from pathlib import Path
import snapsnare
from snapsnare.system import utils
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account

properties = {
    'current.dir': os.path.abspath(os.getcwd()),
    'package.dir': os.path.dirname(snapsnare.__file__),
    'home.dir': str(Path.home()),
    'app.name': 'snapsnare'
}

settings = utils.load_json(properties, 'snapsnare.json')
service_account_file = settings['google']['service_account']
print(service_account_file)


SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/gmail.labels']

path = Path.home() / ".snapsnare" / service_account_file
credentials = ServiceAccountCredentials.from_json_keyfile_name(path, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

results = service.files().list(
    pageSize=10, fields="nextPageToken, files(id, name)").execute()

print(results)

credentials = service_account.Credentials.from_service_account_file(path, scopes=SCOPES)
delegate_credentials = credentials.with_subject('janripke@gmail.com')

service = build('drive', 'v3', credentials=credentials)

results = service.files().list(
    pageSize=10, fields="nextPageToken, files(id, name)").execute()

print(results)


service = build('gmail', 'v1', credentials=delegate_credentials)



results = service.users().labels().list(userId='janripke@gmail.com').execute()