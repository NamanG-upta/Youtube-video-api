import os
import logging
# Google API
from apiclient.discovery import build
import apiclient

from .models import *
from youtube_fetch_api import settings
from datetime import datetime, timedelta
logger = logging.getLogger("application")


def get_response_from_valid_api_key():
    apiKeys = settings.GOOGLE_API_KEYS
    last_request_time = datetime.now() - timedelta(minutes=10)

    status_code = None
    valid = False

    for apiKey in apiKeys:
        try:
            youtube = build("youtube", "v3", developerKey=apiKey)
            request = youtube.search().list(
                q="cricket", 
                part="snippet", 
                order="date", 
                maxResults=50,
                publishedAfter=(last_request_time.replace(microsecond=0).isoformat()+'Z')
            )
            result = request.execute()
            valid = True
        except apiclient.errors.HttpError as err:
            status_code = err.resp.status
            if not(status_code == 400 or status_code == 403):
                break

        if valid:
            #  we found a valid api key so we break out of here, so we return the api response
            return result

    return None

def fetch_videos_from_youtube_and_store_in_db():
    
    response = get_response_from_valid_api_key()

    if response is None:
        logger.info("Invalid response received")
        return

    for item in response['items']:
        
        video_id = item['id']['videoId']
        publishedDateTime = item['snippet']['publishedAt']
        title = item['snippet']['title']
        description = item['snippet']['description']
        thumbnailsUrls = item['snippet']['thumbnails']['default']['url']
        channel_id = item['snippet']['channelId']
        channel_title = item['snippet']['channelTitle']

        Videos.objects.create(
            video_id=video_id,
            title=title,
            description=description,
            channel_id=channel_id,
            channel_title=channel_title,
            publishedDateTime=publishedDateTime,
            thumbnailsUrls=thumbnailsUrls,
        )
    
    logger.info("Objects created succefully")