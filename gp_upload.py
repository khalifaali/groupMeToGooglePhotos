__author__ = 'Khalif Ali'
from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path
from googleapiclient.discovery import build
import requests
import json

...


def authorize(cred_file):
    if not (Path(cred_file).exists()):
        print('File does not exist')
        return None

    flow = InstalledAppFlow.from_client_secrets_file(
        cred_file,
        scopes=['https://www.googleapis.com/auth/photoslibrary.sharing',
                'https://www.googleapis.com/auth/photoslibrary.readonly'])

    credentials = flow.run_local_server(host='localhost',
                                        port=3030,
                                        authorization_prompt_message='Please visit this URL: {url}',
                                        success_message='The auth flow is complete; you may close this window.',
                                        open_browser=True)

    print(dir(credentials))
    return credentials


# this will be the main method we call to run
# because we will need to pass the photos_service around to other methods.
# No other methods can run without this method being called first
def build_photos_service():
    # cred_file = input("enter cred file")
    creds = authorize('credentials.json')

    photos_service = build('photoslibrary', 'v1', credentials=creds)
    # print(dir(photos_service.albums()))
    # albums = photos_service.albums().list().execute()
    return photos_service


def create_album(photos_service, album_name):
    # test to see what is in the create method
    resp = photos_service.albums().create(body={'album':{'title':album_name}}).execute()
    print(json.dumps(resp, indent=3))


# do albums().share(push album id)
# create function to share album


'''
Example:
{
"album": {"title": "New Album Title"}
}

Need a way to comb through the photos and upload them,
So I will need access to the current directory structure and pull back the names of the files

'''


def run():
    photos_service = build_photos_service()

    create_album(photos_service, 'test')


run()

# Redirect the user to auth_uri on your platform.
# credentials = flow.step2_exchange(code)
