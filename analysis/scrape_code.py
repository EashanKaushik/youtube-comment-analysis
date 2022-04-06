import os
import time
import pandas as pd
import sys
from apiclient.discovery import build

def scrape_comments(youtube, ID, directory):
    
    box = [['Name', 'Comment', 'Time', 'Likes', 'Reply Count']]
    
    data = youtube.commentThreads().list(part='snippet', videoId=ID, maxResults='100', textFormat="plainText").execute()
    print('req 1')
    for i in data["items"]:

        name = i["snippet"]['topLevelComment']["snippet"]["authorDisplayName"]
        comment = i["snippet"]['topLevelComment']["snippet"]["textDisplay"]
        published_at = i["snippet"]['topLevelComment']["snippet"]['publishedAt']
        likes = i["snippet"]['topLevelComment']["snippet"]['likeCount']
        replies = i["snippet"]['totalReplyCount']

        box.append([name, comment, published_at, likes, replies])

    while ("nextPageToken" in data):
        
        try:
            data = youtube.commentThreads().list(part='snippet', videoId=ID, pageToken=data["nextPageToken"],
                                             maxResults='100', textFormat="plainText").execute()
        except Exception:
            print('sleeping')
            time.sleep(100)
            data = youtube.commentThreads().list(part='snippet', videoId=ID, pageToken=data["nextPageToken"],
                                             maxResults='100', textFormat="plainText").execute()

        for i in data["items"]:
            name = i["snippet"]['topLevelComment']["snippet"]["authorDisplayName"]
            comment = i["snippet"]['topLevelComment']["snippet"]["textDisplay"]
            published_at = i["snippet"]['topLevelComment']["snippet"]['publishedAt']
            likes = i["snippet"]['topLevelComment']["snippet"]['likeCount']
            replies = i["snippet"]['totalReplyCount']

            box.append([name, comment, published_at, likes, replies])

    df = pd.DataFrame({'Name': [i[0] for i in box], 'Comment': [i[1] for i in box], 'Time': [i[2] for i in box],
                       'Likes': [i[3] for i in box], 'Reply Count': [i[4] for i in box]})

    df.to_csv(os.path.join(directory, f'{ID}.csv'), index=False, header=False)

    print(f"Successful! Check the {ID} CSV file that you have just created.")


if __name__ == '__main__':
    
    url_code = sys.argv[1]
    API_KEY = sys.argv[2]
    
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    scrape_comments(youtube=youtube, ID=url_code, directory='build/comment_data')
    