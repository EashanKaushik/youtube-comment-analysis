import os

def scrape_comments(youtube, ID, directory):
    
    box = [['Name', 'Comment', 'Time', 'Likes', 'Reply Count']]
    
    data = youtube.commentThreads().list(part='snippet', videoId=ID, maxResults='100', textFormat="plainText").execute()

    for i in data["items"]:

        name = i["snippet"]['topLevelComment']["snippet"]["authorDisplayName"]
        comment = i["snippet"]['topLevelComment']["snippet"]["textDisplay"]
        published_at = i["snippet"]['topLevelComment']["snippet"]['publishedAt']
        likes = i["snippet"]['topLevelComment']["snippet"]['likeCount']
        replies = i["snippet"]['totalReplyCount']

        box.append([name, comment, published_at, likes, replies])

        # totalReplyCount = i["snippet"]['totalReplyCount']

        # if totalReplyCount > 0:

        #     parent = i["snippet"]['topLevelComment']["id"]

        #     data2 = youtube.comments().list(part='snippet', maxResults='100', parentId=parent,
        #                                     textFormat="plainText").execute()

        #     for i in data2["items"]:
        #         name = i["snippet"]["authorDisplayName"]
        #         comment = i["snippet"]["textDisplay"]
        #         published_at = i["snippet"]['publishedAt']
        #         likes = i["snippet"]['likeCount']
        #         replies = ""

        #         box.append([name, comment, published_at, likes, replies])

    while ("nextPageToken" in data):

        data = youtube.commentThreads().list(part='snippet', videoId=ID, pageToken=data["nextPageToken"],
                                             maxResults='100', textFormat="plainText").execute()

        for i in data["items"]:
            name = i["snippet"]['topLevelComment']["snippet"]["authorDisplayName"]
            comment = i["snippet"]['topLevelComment']["snippet"]["textDisplay"]
            published_at = i["snippet"]['topLevelComment']["snippet"]['publishedAt']
            likes = i["snippet"]['topLevelComment']["snippet"]['likeCount']
            replies = i["snippet"]['totalReplyCount']

            box.append([name, comment, published_at, likes, replies])

            # totalReplyCount = i["snippet"]['totalReplyCount']

            # if totalReplyCount > 0:

            #     parent = i["snippet"]['topLevelComment']["id"]

            #     data2 = youtube.comments().list(part='snippet', maxResults='100', parentId=parent,
            #                                     textFormat="plainText").execute()

            #     for i in data2["items"]:
            #         name = i["snippet"]["authorDisplayName"]
            #         comment = i["snippet"]["textDisplay"]
            #         published_at = i["snippet"]['publishedAt']
            #         likes = i["snippet"]['likeCount']
            #         replies = ''

            #         box.append([name, comment, published_at, likes, replies])

    df = pd.DataFrame({'Name': [i[0] for i in box], 'Comment': [i[1] for i in box], 'Time': [i[2] for i in box],
                       'Likes': [i[3] for i in box], 'Reply Count': [i[4] for i in box]})

    df.to_csv(os.path.join(directory, f'{ID}.csv'), index=False, header=False)

    print(f"Successful! Check the {ID} CSV file that you have just created.")
