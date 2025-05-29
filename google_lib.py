import os
import pickle
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# The scope needed for reading your albums
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

# Token pickle file (to store tokens between runs)
TOKEN_PICKLE = 'token.pickle'

# authentication function: --------------------------------------
def authenticate():
    creds = None
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as token:
            creds = pickle.load(token)
    # If no valid creds, do OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)  # Opens a browser for login
        # Save the credentials for next time
        with open(TOKEN_PICKLE, 'wb') as token:
            pickle.dump(creds, token)

    service = build('photoslibrary', 'v1', credentials=creds, static_discovery=False)
    return service

# get all albums ----------------------------------------------------------------------
def fetch_all_albums(service):
    albums = []
    next_page_token = None

    # Fetch all albums
    while True:
        result = service.albums().list(pageSize=50, pageToken=next_page_token).execute()
        albums.extend(result.get('albums', []))
        next_page_token = result.get('nextPageToken')
        if not next_page_token:
            break

    # only retrieve those 3 attributes:
    albums2 = []
    for album in albums:
        albums2.append({
            "id": album['id'],
            "title": album['title'],
            "mediaItemsCount": album["mediaItemsCount"]
            })

    return albums2

# get all media ----------------------------------------------------------------------
def fetch_all_media(service):
    objs = []
    next_page_token = None

    # Fetch all albums
    while True:
        result = service.mediaItems().list(pageSize=50, pageToken=next_page_token).execute()
        objs.extend(result.get('mediaItems', []))
        next_page_token = result.get('nextPageToken')
        if not next_page_token:
            break

    # only rterieve some attributes
    media_list = []
    for media in objs:
        media_list.append({
                'id': media['id'], 
                'creationTime': media['mediaMetadata']['creationTime'],
                'filename': media['filename']
                }
                )

    return media_list

# create link between albums and items: ---------------------------------------
def fetch_media_per_album(service, album_id):
    itemlist = []
    next_page_token = None

    # Fetch all albums
    while True:
        result = service.mediaItems().search(
            body={
                "albumId": album_id,
                "pageSize": 50,
                "pageToken": next_page_token
            }
        ).execute()
        itemlist.extend(result.get('mediaItems', []))
        next_page_token = result.get('nextPageToken')
        if not next_page_token:
            break

    # only fetch ids:
    id_list = []
    for item in itemlist:
        id_list.append(item['id'])
        
    return id_list

# for exporting to json:
def saving2json(object, fname):
    with open(fname, 'w', encoding='utf-8') as f:
        json.dump(object, f, ensure_ascii=False, indent=2)
    return 1

def main():

    print("START....")
    service = authenticate()
    
    print("AUTHENTICATION SUCCESSFUL")
    print('----')
    print("  fetching albums...")
    albums = fetch_all_albums(service)
    save_response = saving2json(albums, "albums.json")
    if save_response == 1:
        print("  saved albums")

    print("  fetching media...")
    media = fetch_all_media(service)
    save_response = saving2json(media, "media.json")
    if save_response == 1:
        print("  saved media")

    print("  fetching media album link...")
    # collect all media to all albums:
    album_collection = []
    for album in albums:
        album_id = album['id']
        media_ids = fetch_media_per_album(service, album_id)
        album_collection.append({'album_id': album_id, 'media_ids': media_ids})

    save_response = saving2json(album_collection, "album_media.json")
    if save_response == 1:
        print("  saved album_media")


if __name__ == '__main__':
    main()
