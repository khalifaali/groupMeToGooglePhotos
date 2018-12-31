__author__ = 'Khalif Ali'
from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path
from googleapiclient.discovery import build
from pprint import pprint
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


def get_album_list(photos_service):
    private_album_list = photos_service.albums().list().execute()
    shared_album_list = photos_service.sharedAlbums().list().execute()
    # we slice everything from the first one because the first objeect the album response doesnt have the title key
    private_album_list = private_album_list['albums'][1:]
    shared_album_list = shared_album_list['sharedAlbums']
    print(json.dumps(shared_album_list, indent=3))
    return [album['title'] for album in private_album_list] + [album['title'] for album in shared_album_list if 'title'
                                                               in album]


def create_shareable_album(photos_service, album_name):
    # test to see what is in the create method
    # album is actually a json response for creation of the album, will have album id, title, productUrl
    current_albums = get_album_list(photos_service)
    pprint(current_albums)
    if album_name in current_albums:
        print('Album already exist')
        print('Aborting creation....')
        return None
    album = photos_service.albums().create(body={'album': {'title': album_name}}).execute()
    print(json.dumps(album, indent=3))
    # shared_album is a json reponse as a result of sharing the album, will have shareable_url,shared_token,isJoined
    shared_album = photos_service.albums().share(albumId=album['id'],
                                                 body={
                                                     "sharedAlbumOptions": {
                                                         "isCollaborative": "true",
                                                         "isCommentable": "true"
                                                     }}).execute()

    print('Album:{} \nShareable Url {}'.format(album['title'], shared_album['shareInfo']['shareableUrl']))


'''
{
  "sharedAlbumOptions": {
    "isCollaborative": "true",
    "isCommentable": "true"
  }
}

Response

'''

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

    create_shareable_album(photos_service, 'teste22')


run()

# Redirect the user to auth_uri on your platform.
# credentials = flow.step2_exchange(code)
