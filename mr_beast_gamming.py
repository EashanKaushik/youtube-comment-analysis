from read_youtube import scrape_comments

api_key = "AIzaSyBDxsT_4J155fDCsY8zlOkjvxaosXa43ts" # Replace this dummy api key with your own.

from apiclient.discovery import build
youtube = build('youtube', 'v3', developerKey=api_key)

import pandas as pd

# ID = ["LnlKwzc_TNA"] # Replace this YouTube video ID with your own.
ID = ["QsUfsZzxi9c", "ABTdTTnnEU8", "xN8ENrfE-TY"]
name = ["Whatever You Build, I'll Pay For!", "World’s Largest Explosion!", "If You Build a House, I'll Pay For It!"]

for vid_id in ID:
    scrape_comments(youtube=youtube, ID=vid_id, directory='mr_beast')