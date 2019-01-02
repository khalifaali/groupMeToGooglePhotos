__author__ = 'Khalif Ali'
import google.auth.transport.requests
from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path
from googleapiclient.discovery import build
from pprint import pprint
import json, requests, os
import pathlib
from glob import glob
import inspect

bearer_token = ''
shared_url = ''
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
                'https://www.googleapis.com/auth/photoslibrary.appendonly',
                'https://www.googleapis.com/auth/photoslibrary'])

    credentials = flow.run_local_server(host='localhost',
                                        port=3030,
                                        authorization_prompt_message='Please visit this URL: {url}',
                                        success_message='The auth flow is complete; you may close this window.',
                                        open_browser=True)


    print(dir(credentials))
    if credentials.expired:
        print('Credentials expired')
        req = google.auth.transport.requests.Request()
        credentials.refresh(req)
        print('Refreshing...')

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
    # using list comprehension return object of objects for album and its album id
    # the ** is used with the inner objects to merge them into a new object
    album_list = {**{album['title']: album['id'] for album in private_album_list if 'title' in album},
                  **{album['title']: album['id'] for album in shared_album_list if 'title' in album}
                  }

    # remove duplicates from album_list
    return album_list


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


def create_media_token(upload_file):

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
        payload = {'file': upload_bytes}
        token_response = requests.post(url=url, headers=headers, data=payload)

    # token successfully created so return it

    # print('status code for token', token_response.text)
    # if status code is good then return the token
    # otherwise return None
    if int(token_response.status_code) == 200:
        return str(token_response.text)
    return None


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

    if album_name in current_albums:
        print('Album already exist')
        print('Aborting creation....')
        print(album_name ,' Already exists ', ' id: ', current_albums[album_name])

        return current_albums[album_name]
    album = photos_service.albums().create(body={'album': {'title': album_name}}).execute()
    # print(json.dumps(album, indent=3))
    # shared_album is a json reponse as a result of sharing the album, will have shareable_url,shared_token,isJoined
    shared_album = photos_service.albums().share(albumId=album['id'],
                                                 body={
                                                     "sharedAlbumOptions": {
                                                         "isCollaborative": "true",
                                                         "isCommentable": "true"
                                                     }}).execute()

    # print('Album:{} \nShareable Url {}'.format(album['title'], shared_album['shareInfo']['shareableUrl']))
    global shared_url
    shared_url = shared_album['shareInfo']['shareableUrl']
    print('shared url ', shared_url)

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


# Need to write method to grab files from a specified directory. Retrieve directories for the user for now
# afterward we will allow you to specify a directory
def grab_directory():
    dirs = []
    pos = 0
    cwd = os.getcwd()
    for dir_contents in Path(cwd).iterdir():
        if dir_contents.is_dir() and not ('.' in dir_contents.name):
            dirs.append(dir_contents.name)
            print('Choice ', pos, 'Directory ', dir_contents.name)
            pos += 1

    choice = int(input("What directory do you want? Please enter index "))

    return dirs[choice]


def grab_files(dir):
    if dir is None:
        # need to autofill directory list and show to the user, else just pull back that directory
        dirs = []
        cwd = os.getcwd()
        pos = 0
        for dir_contents in Path(cwd).iterdir():
            if dir_contents.is_dir() and not ('.' in dir_contents.name):
                dirs.append(cwd + '\\' + dir_contents.name)
                print('Choice ', pos, 'Directory ', dir_contents.name)
                pos += 1

        choice = int(input("What directory do you want? Please enter index "))

        pprint(dirs[choice])
        dir = dirs[choice]

        # we glob for all images and videos in the directory
    return glob(dir + '\\*')

    # might have to check if the file is a video or jpeg


def run():
    # Don't forget to allow the user to supply name of their cred file
    # TODO: Now we need to loop through all the directories and get upload tokens for the files

    token_list = []
    # pload_files = grab_files()
    photos_service = build_photos_service()
    # a_list = get_album_list(photo_service)
    # TODO rename grab_directory to get_target_directory, and grab_files to get_target_files or get_upload_files
    # photos_service = build_photos_service()
    target_directory = grab_directory()

    album_id = create_shareable_album(photos_service, target_directory)
    print('You chose this directory ', target_directory)
    upload_files = grab_files(target_directory)
    pprint(upload_files, indent=1)

    # pprint(a_list, indent=1)

    newMediaItems = {'newMediaItems': [],'albumId':album_id
                     }


    # we need the albumId of a particular album from the shared directory
    # which we will actually get from creating the shareable album so we dont need to call get album list fr fr
    # so now we need to get the target directory name for testing
    # write quick function to pull back directory name and pass it
    headers = {
        'Authorization': "Bearer " + bearer_token,
        'Content-Type': 'application/json',
    }
    url = 'https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate'
    media_list = []
    for file in upload_files:

        # I think we had to do it like this because it was accessing the same reference
        # so when we recreate it we (i guess) get a new reference to put a media token too
        simpleMediaItem = {'simpleMediaItem':
                           {'uploadToken': ''},
                           'description': 'just work'
                   }
        simpleMediaItem['simpleMediaItem']['uploadToken'] = create_media_token(file)

        #print('Simple Media Item obj', simpleMediaItem)
        media_list.append(simpleMediaItem)

    pprint(media_list, indent=2)
    newMediaItems['newMediaItems'] = media_list

    resp = photos_service.mediaItems().batchCreate(body=newMediaItems).execute()
    pprint(resp, indent=2)




        # resp = requests.post(url, data=req_body, headers=headers)


        # pprint(resp, indent=2)




    # batch Create MediaItems
    # print(inspect.getfullargspec(photos_service.mediaItems().batchCreate()))


    # so we need to append to newMediaItems then access simpleMediaItem then access upload token and set that to
    #   the return value of create_media_item
    # token_list.append(create_media_token(photos_service,file,))


    print('Amount of files grabbed ', len(upload_files))


run()

# Redirect the user to auth_uri on your platform.
# credentials = flow.step2_exchange(code)
