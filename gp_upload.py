__author__ = 'Khalif Ali'
from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path
from googleapiclient.discovery import build
from pprint import pprint
import json, requests
from requests import Request, Session

bearer_token = ''
...
'''
SCOPE:https://www.googleapis.com/auth/photoslibrary	
--Access to both the .appendonly and .readonly scopes. 

SCOPE:https://www.googleapis.com/auth/photoslibrary.sharing	
--Access to sharing calls.
--Access to create an album, share it, upload media items to it, and join a shared album.


'''

def authorize_service(cred_file):
    if not (Path(cred_file).exists()):
        print('File does not exist')
        return None

    flow = InstalledAppFlow.from_client_secrets_file(
        cred_file,
        scopes=['https://www.googleapis.com/auth/photoslibrary.sharing',
                'https://www.googleapis.com/auth/photoslibrary'])

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
    creds = authorize_service('credentials.json')
    global bearer_token
    bearer_token = str(creds.token)
    print('bearer token : ', bearer_token)

    photos_service = build('photoslibrary', 'v1', credentials=creds)
    # print(dir(photos_service.albums()))
    # albums = photos_service.albums().list().execute()
    return photos_service


def get_album_list(photos_service):
    private_album_list = photos_service.albums().list().execute()
    shared_album_list = photos_service.sharedAlbums().list().execute()
    '''
      we slice everything from the first one because the first objeect the 
    private album response doesnt have the title key
    '''
    private_album_list = private_album_list['albums'][1:]
    shared_album_list = shared_album_list['sharedAlbums']
    # print(json.dumps(shared_album_list, indent=3))
    return [album['title'] for album in private_album_list] + \
           [album['title'] for album in shared_album_list if 'title' in album]


'''
Need to comb through the current directory, go through the file and create them in batch
Read file bytes upload them, and push token to an array 
Continue to do this then call batch create

Now this where
'''

# Need specific album id to do the upload properly after bytes are sent to google server
# TODO: Need to create a post request to send to google server with file bytes
'''
Post request details

POST https://photoslibrary.googleapis.com/v1/uploads
Authorization: Bearer OAUTH2_TOKEN
Content-type: application/octet-stream
X-Goog-Upload-File-Name: FILENAME
X-Goog-Upload-Protocol: raw

'''


def create_media_token(photos_service, upload_file, album_id):
    session = Session()
    print(bearer_token)
    if not Path(upload_file).exists():
        print('File does not exists')
        return None

    headers = {'Authorization': 'Bearer ' + bearer_token,
               'Content-type': 'application/octet-stream',
               'X-Goog-Upload-File-Name': upload_file,
               'X-Goog-Upload-Protocol': 'raw'}

    url = 'https://photoslibrary.googleapis.com/v1/uploads'
    # url to that we use to upload media items to google server
    # Our next request will use the album id to upload it
    with open(upload_file, 'rb') as file:
        upload_bytes = file.read()
        payload = {'file':upload_bytes}
        token_response = requests.post(url=url,headers=headers,data=payload)

    # token successfully created so return it
   
    # print('status code for token', token_response.text)
    return token_response.text



'''

Request body to add media items to google photos after byte upload
{
"albumId": "ALBUM_ID",
"newMediaItems": [
{
  "description": "ITEM_DESCRIPTION",
  "simpleMediaItem": {
    "uploadToken": "UPLOAD_TOKEN"
  }
}
, ...
]
}

'''


def create_shareable_album(photos_service, album_name):
    # test to see what is in the create method
    # album contains a json response describing the created album, will have album id, title, productUrl
    current_albums = get_album_list(photos_service)
    pprint(current_albums)
    if album_name in current_albums:
        print('Album already exist')
        print('Aborting creation....')
        return None
    album = photos_service.albums().create(body={'album': {'title': album_name}}).execute()
    # print(json.dumps(album, indent=3))
    # shared_album is a json reponse as a result of sharing the album, will have shareable_url,shared_token,isJoined
    shared_album = photos_service.albums().share(albumId=album['id'],
                                                 body={
                                                     "sharedAlbumOptions": {
                                                         "isCollaborative": "true",
                                                         "isCommentable": "true"
                                                     }}).execute()

    print('Album:{} \nShareable Url {}'.format(album['title'], shared_album['shareInfo']['shareableUrl']))
    return album['id']


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
    # Don't forget to allow the user to supply name of their cred file
    token_list = []
    photos_service = build_photos_service()
    aid = create_shareable_album(photos_service, 'last onleakl ka.ld.lw.a/.')
    '''
    Token will be returned from create_media_token loop throuogh directory sending each file to the google server
     and push all returned upload tokens to an array
     
     consider renaming upload_media_token to create_media_token
    '''
    token = create_media_token(photos_service,'.\\AUC ANIMEWATCHERS UNITED CAMPUS\\154584922655919800.jpeg',
                       aid)
    token_list.append(token)
    print(token_list)



run()

# Redirect the user to auth_uri on your platform.
# credentials = flow.step2_exchange(code)
