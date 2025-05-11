# Google Sheets API Imports
from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import json

import requests
import time
from datetime import datetime

DEBUG = False

# SLEEP_TIMER = 3600 # sleep for 1 hour
SLEEP_TIMER = 900 # sleep for 15 mins
SLOW_SLEEP_TIMER = 3600 # sleep for 1h

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]


USERNAME = "SOPD Ballers"; 
AVATAR_URL = "https://yt3.googleusercontent.com/iITluvBkSaSTQeKScFbpE5V4CKJl7mNnrfneeLoGzEZ8YHNdsf9KjX75y9etRSb4Ibwdvb7uCJ4=s160-c-k-c0x00ffffff-no-rj";

# // The URL of your Discord webhook
# TEST_WEBHOOK_URL = "https://discord.com/api/webhooks/1358344057079988374/sQjj9_xuZm21Jsy7FfYbFt_jbCAllj92agMrsYhUhFAWjegt4lNaceUQCXCw4k3Cecxz"
# WEBHOOK_URL = TEST_WEBHOOK_URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1356520107010166874/hv1Lf-yGguIIX8uO34HdPJ3363ILQ3_cmjMGL4fnP0pUJBNcD3bl3yNNAVSkXOlV0yjY"; 

# playlists to Monitor
CHANNEL_ID = "UCI1RCT47NuGEDxTfwiwBVLg"

# Playlists subscribed
S_ELV_PLAYLIST_ID = "PLMv_MOdIUtdKNBx3u_V6UR4-JvG-oTlvE"
S_RED_PLAYLIST_ID = "PLMv_MOdIUtdL5gaFEYlZg1lkGJMPUgHkf"
S_KIRK_PLAYLIST_ID = "PLMv_MOdIUtdJd3PLSLoCng19CJTgVDPnt"
S_AVL_PLAYLIST_ID = "PLMv_MOdIUtdLuA0ggNn7294qfH9D2VcLb"
SCVC_DRILLS_PLAYLIST_ID = "PLMv_MOdIUtdKRPtukJR5b3CNHxVrBUE3R"
SOPD_PLAYLIST_ID = "PLMv_MOdIUtdIdZ6DG9r_lTIArhjMfWUdv"
S_MISC_PLAYLIST_ID = "PLMv_MOdIUtdLJ4S0uSKL2napYRIsQZO99"

SUBSCRIBED_PLAYLISTS = [S_AVL_PLAYLIST_ID, S_ELV_PLAYLIST_ID, S_RED_PLAYLIST_ID, S_KIRK_PLAYLIST_ID, SCVC_DRILLS_PLAYLIST_ID, SOPD_PLAYLIST_ID, S_MISC_PLAYLIST_ID]
if DEBUG:
    SUBSCRIBED_PLAYLISTS = [S_RED_PLAYLIST_ID]

# Other playlists
W_RED_TEMP_PLAYLIST_ID = "PLMv_MOdIUtdLrxxk87uogylhGKfhXfALQ"
LA_FITNESS_PLAYLIST_ID = "PLMv_MOdIUtdKV93qAzEzb36EXUxTF5mYt"
W_MISC_PLAYLIST_ID = "PLMv_MOdIUtdITcGzYTfaglXtYCMDAw9IU"
W_KIRK_PLAYLIST_ID = "PLMv_MOdIUtdIX1tQTwX03JSIc-5qPRhBc"
W_AVL_PLAYLIST_ID = "PLMv_MOdIUtdKvle61fhLGDO38kbdgc39t"
SCVC_PLAYLIST_ID = "PLMv_MOdIUtdKrvKlwZ0XYr2dcteU96iSv"
TOURNEY_PLAYLIST_ID = "PLMv_MOdIUtdKOuhVpj4yyBl4XHPX-T0if"

DATA_FOLDER = "data"
DATA_FILE = f"{DATA_FOLDER}/data.json"
TEST_DATA_FILE = f"{DATA_FOLDER}/test_data.json"


PLAYLIST_URL = "https://www.youtube.com/playlist?list="
YOUTUBE_SHORT_URL = "https://youtu.be/"

def GetPlaylistURL(playlistId):
    return f"{PLAYLIST_URL}{playlistId}"

# https://youtu.be/XpFzdrr_B3s?list=PLMv_MOdIUtdLJ4S0uSKL2napYRIsQZO99
def GetVideoURLWithPlaylist(videoId, playlistId):
    return f"{YOUTUBE_SHORT_URL}{videoId}?list={playlistId}"

class Database():
    def add(self, data):
        playlist = {
            "id":data["id"],
            "title": data["title"],
            "numVideos": data["numVideos"]
            }
        
        self.playlists.append(playlist)
    
    def updated(data):
        pass
        
class Youtube:    
    def __init__(self):
        self.service = self.setupYoutubeAPI()

    def setupYoutubeAPI(self):
        print("Setting up connection to Youtube API...")

        api_service_name = "youtube"
        api_version = "v3"
        
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build(api_service_name, api_version, credentials=creds)
        return service

    # unused
    def fetchChannelPlaylists(self, channelId):
        request = self.service.playlists().list(
            part="contentDetails,id,snippet",
            channelId=channelId,
            maxResults=50, # TODO: once there's more than 50 playlists, we need to update this code to use `nextPageToken`
        )
        response = request.execute()

        channel = {"channelId ": channelId,
                   "playlists": [
                       {"id":playlist["id"],
                        "title": playlist["snippet"]["title"],
                        "numVideos": playlist["contentDetails"]["itemCount"] } for playlist in response["items"]]
        }
        
        with open(DATA_FILE, 'w') as file:
            json.dump(channel, file, indent=2)

    def fetchPlaylist(self, playlistId):
        request = self.service.playlistItems().list(
            part="contentDetails, id, snippet, status",
            maxResults=50,
            playlistId=playlistId
        )
        response = request.execute()
        time.sleep(2)
        numResults = response["pageInfo"]["totalResults"]
        if DEBUG:
            print(response)
        
        videos= {}
        for video in response["items"]:
            videos[video["id"]] = {"title": video["snippet"]["title"],
                                   "videoId": video["contentDetails"]["videoId"],
                                   "playlistId": playlistId,
                                   "uploaded": True if video["snippet"]["thumbnails"].get("maxres") else False}
        
        while "nextPageToken" in response:
            request = self.service.playlistItems().list(
                part="contentDetails, id, snippet",
                maxResults=50,
                playlistId=playlistId,
                pageToken=response["nextPageToken"]
                )
            response = request.execute()
            time.sleep(2)
            for video in response["items"]:
                videos[video["id"]] = {"title": video["snippet"]["title"],
                                       "videoId": video["contentDetails"]["videoId"],
                                       "playlistId": playlistId,
                                       "uploaded": True if video["snippet"]["thumbnails"].get("standard") else False}
            # print(response)
        return numResults, videos

def loadData():
    with open(DATA_FILE, 'r') as file:
        return json.load(file)
    
def saveData(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=2)
    
def loadTestData():
    with open(TEST_DATA_FILE, 'r') as file:
        return json.load(file)

def postVideoUpdateToDiscord(video):
    url = WEBHOOK_URL
    headers = {
        "Content-type": "application/json",
    }
    data = {
        "username": USERNAME,
        "avatar_url": AVATAR_URL,
        "content": f"Hey Ballers, New Video just dropped!\n    **{video.get('title')}**: {GetVideoURLWithPlaylist(video.get('videoId'), video.get('playlistId'))}",
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response)

def postUpdateToDiscord(videos):
    
    numVideos = len(videos)
    if(numVideos == 0):
        return
    
    if(numVideos == 1):
        postVideoUpdateToDiscord(videos[0])
        return
        
    
    url = WEBHOOK_URL
    headers = {
        "Content-type": "application/json",
    }
    
    content = f"Hey Ballers, We got {numVideos} New Videos for y'all!"
    for video in videos:
        content += f"\n    **{video.get('title')}**: {GetVideoURLWithPlaylist(video.get('videoId'), video.get('playlistId'))}"
    data = {
        "username": USERNAME,
        "avatar_url": AVATAR_URL,
        "content": content,
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response)
    
def postNewPlaylistToDiscord(playlistId):
    url = WEBHOOK_URL
    headers = {
        "Content-type": "application/json",
    }
    data = {
        "username": USERNAME,
        "avatar_url": AVATAR_URL,
        "content": f"Hey Ballers, New Playlist just dropped!\n    {GetPlaylistURL(playlistId)}",
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response)

youtube = Youtube()
oldData = loadData()
if DEBUG:
    oldData = loadTestData()
# time.sleep(3600*8)
outOfDate = False
while True:
# if True:


    # Get the current date and time
    now = datetime.now()

    # Print the current date and time
    print(f"[{now}]")
    updated = False
    allUploaded = True
    newData = {}
    for playlistId in SUBSCRIBED_PLAYLISTS:
        numVideos, videos = youtube.fetchPlaylist(playlistId)
        newData[playlistId] = {"count":numVideos, "videos":videos}
    
    if DEBUG:
        break
    
    # saveData(newData)
    for playlistId in SUBSCRIBED_PLAYLISTS:
        oldPlaylist = oldData.get(playlistId)
        newPlaylist = newData.get(playlistId)
        
        if oldPlaylist is None:
            # New playlist
            print(playlistId, "New Playlist")
            updated = True
            postNewPlaylistToDiscord(playlistId)
        else:
            newVideos = []
            videosUploading = []
            for key, value in newPlaylist["videos"].items():
                if key not in oldPlaylist["videos"].keys(): # new video
                    if not value["uploaded"]: # not finished uploading.
                        videosUploading.append(value)
                    else:
                        newVideos.append(value)
                elif not oldPlaylist["videos"][key]["uploaded"]: # previously uploading video
                    if value["uploaded"]: #done uploading
                        # print(f"adding {value} since {key} done uploading")
                        newVideos.append(value)
                    else: # still uploading
                        videosUploading.append(value)
        
            if videosUploading != []:
                # videos are still uploading
                print(playlistId, f"{len(videosUploading)} video(s) are still uploading...\t{len(newVideos)} video(s) ready to report...")
                allUploaded = False
                continue
            
            if newVideos != []:
                print(playlistId, f"{len(newVideos)} videos to update")
                postUpdateToDiscord(newVideos)
                updated = True
                outOfDate = True
            else:
                print(playlistId, "No videos to update")
    
    if updated:
        oldData = newData
        
    if outOfDate and allUploaded:
        saveData(newData)
        oldData = loadData()
        outOfDate = False

    timer = SLEEP_TIMER if not allUploaded else SLOW_SLEEP_TIMER
    print(f"sleeping for {timer} seconds...\n")
    time.sleep(timer)
