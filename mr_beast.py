from read_youtube import scrape_comments

api_key = "AIzaSyBDxsT_4J155fDCsY8zlOkjvxaosXa43ts" # Replace this dummy api key with your own.

from apiclient.discovery import build
youtube = build('youtube', 'v3', developerKey=api_key)

import pandas as pd

# ID = ["LnlKwzc_TNA"] # Replace this YouTube video ID with your own.
ID = ["0e3GPea1Tyg", "r7zJ8srwwjk", "9bqk6ZUsKyA"]
name = ["$456,000 Squid Game In Real Life!", "I Spent 50 Hours In Solitary Confinement", "I Spent 50 Hours Buried Alive"]

for vid_id in ID:
    scrape_comments(youtube=youtube, ID=vid_id, directory='mr_beast_gaming')