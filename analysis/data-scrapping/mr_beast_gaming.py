from read_youtube import scrape_comments
import environ
import os
import sys
from apiclient.discovery import build

environ.Env.read_env()

youtube = build("youtube", "v3", developerKey=os.environ[str(sys.argv[1])])

import pandas as pd

# ID = ["LnlKwzc_TNA"] # Replace this YouTube video ID with your own.
ID = ["QsUfsZzxi9c", "ABTdTTnnEU8", "xN8ENrfE-TY"]
name = [
    "Whatever You Build, I'll Pay For!",
    "World’s Largest Explosion!",
    "If You Build a House, I'll Pay For It!",
]

for vid_id in ID:
    scrape_comments(youtube=youtube, ID=vid_id, directory="mr_beast_gaming")
