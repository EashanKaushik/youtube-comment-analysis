from read_youtube import scrape_comments
import environ
import os
import sys
from apiclient.discovery import build

environ.Env.read_env()

youtube = build("youtube", "v3", developerKey=os.environ[sys.argv[1]])

import pandas as pd

# ID = ["LnlKwzc_TNA"] # Replace this YouTube video ID with your own.
ID = ["0e3GPea1Tyg", "r7zJ8srwwjk", "9bqk6ZUsKyA"]
name = [
    "$456,000 Squid Game In Real Life!",
    "I Spent 50 Hours In Solitary Confinement",
    "I Spent 50 Hours Buried Alive",
]

# for vid_id in ID:
scrape_comments(youtube=youtube, ID=ID[0], directory="mr_beast")
