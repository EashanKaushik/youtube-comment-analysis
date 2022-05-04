# Youtube Comment Analysis(YCA) using Vader and LSTM

## Demo Video

[![Watch the video](https://user-images.githubusercontent.com/50113394/166615655-04172008-e0f0-420b-b117-c8b4ff5691d7.png)](https://youtu.be/BNPqXxj8aqg)

## Introduction

In this project, we will not only prepare our own dataset of YouTube comments, but also will classify these comments into three categories namely Positive, Negative and Neutral. The data will be fed into Valence Aware Dictionary for Sentiment Reasoning (Vader) algorithm this will give us the polarity of sentiment and intensity of emotion. Using these parameters we will assign each comment the aforementioned categories. Now that we have target labels present in our dataset, we plan to train a supervised learning algorithm like LSTM to classify unlabeled data. 

The end goal of the project would be to provide the user with a UI interface in which they can upload an URL of any YouTube video and the application will classify the comments into the above-mentioned labels, giving the user an idea of how the video might be in terms of quality.

## Data Scraping 

The dataset we are using is scrapped by us. This data consists of 5 columns namely, Name of the Author of the Comment, the Comment itself, Time at which comment was posted, likes on the Comment and Reply to the comment. These comments are exclusively from the most popular videos on Mr. Beast Channel and Mr. Beast Gaming Channel.

In order to get the dataset for this project we developed a code using YouTube API deployed on AWS for comment mining. This code is responsible for data scrapping on server side with no overhead to the client. Till now we have managed to mine over 1 million comments. Most of the comments in the video are neutral or positive not many negative comments. 

This data is stored in a private S3 bucket; therefore, nobody would be able to view the scrapped comments from S3. We have provided a Google Drive link for the Dataset as well, [Dataset](https://www.kaggle.com/datasets/eashankaushik/youtube-scrapped-data).

Steps to get scrap data: -
1. Get the code of the video you want to scrap. 
2. Enter the code in the URL Tab. 
3. Copy the request ID and go to the request tab. 
4. Enter the request and hit submit. 
5. If the data is scrapped it will show data is scrapped or else request pending. 

Pipeline for obtaining the data: -

<p align="center">
  <img src="https://user-images.githubusercontent.com/50113394/166609932-726f1177-162d-4cfd-800b-40bfc9cb6452.png" />
</p>

### Dataset

We have scrapped over 1,507,306 comments for our problem statement. These comments are exclusively from the most popular videos on Mr. Beast Channel and Mr. Beast Gaming Channel. Each row in the dataset constitutes of 5 columns namely Name of the Author of the Comment, the Comment itself, Time at which comment was posted, likes on the Comment and Reply to the comment. 
As you can see, we do not have the target variable for our problem statement, sentiment of the comment at this time. And if we choose to solve the given problem, we can use unsupervised learning algorithms like Clustering for classifying the comments into Positive, Negative and Neutral. To get some idea as to how many comments we have mined based on the target variables (Postive, Negative and Neutral) we have used Vader for Sentiment Analysis. In the following graph you can see the distribution of comments among the target variables. 


<p align="center">
  <img src="https://user-images.githubusercontent.com/50113394/166609977-d34c9792-f343-4acb-b883-f20b76bad42a.png" />
</p>

This type of distribution is expected. Majority of the comments on any YouTube Videos are meaningless, and most of the time are not talking about the Video itself. Example, comments like advertisement for other YouTube Channel, comments like ‘Hi’, ‘First’, etc. . Since Mr. Beast is one of the most popular YouTuber and most of the videos are about helping individuals, the sentitment around his videos is Positive. However, that being said, some of viewers are of mindset that giving people insane amount of money might be degrading sometimes. All these claims are proven in the Figure 5.   

We have used Vader for generating labels Negative, Positive and Neutral. After we have extracted these labels, we see that we have an imbalanced dataset as seen in the figure above. To address this issue we have taken around 200,000 comments from Positve and Neutral class and 182,000 from Negative class. Newly distributed dataset can be viewed here: [Dataset](https://www.kaggle.com/datasets/eashankaushik/youtube-scrapped-data?select=dataset.csv). 

<p align="center">
  <img src="https://user-images.githubusercontent.com/50113394/166610657-c2fde8f1-0c91-4eda-9258-770d77ddaad5.png" />
</p>

## Sentiment Anlysis

<p align="center">
  <img src="https://user-images.githubusercontent.com/50113394/166610019-00118e51-ee39-4493-868b-1fc9de4bb96e.png" />
</p>

We have considered two ways to validate our models. The first of them being splitting the data into an 80/20 split of training and testing dataset. This is because then we can make use of most of the data for training purposes and then use just a small portion for testing. This in turn would give us an idea of how well our machine learning model performs. 

Secondly, we have calculated validation accuracy of our LSTM model which tells us how efficiently our model has worked using the test data. In our case we ran a total of three epochs which gave us a validation accuracy of 0.9814, 0.9822, 0.9833 respectively and training accuracy of 0.9577, 0.9861 and 0.9901. This is a good sign that our model is not overfiting or underfiting the dataset and is generalizing well to unseen data. 


## Conclusion 

The number of comments on a popular YouTube video is huge. It is difficult to make sense of it by the viewer or even the Youtuber. We plan to develop a fully functional website, in which the user needs to enter the YouTube video code. After this, we will scrap the data and provide the user with a brief analysis of comments on the video. This will give the users another metric to rate the video. Also this will help the youtuber to know the public consensus around their video. 

This application was developed using Django Python Framework. The data is stored in a S3 bucket and our application uses python boto3 to get data from the bucket. For production purposes we have stored our trained LSTM model and other necessary files in a public S3 bucket. Necessary files can be downloaded here, [tokenizer](https://yca-analytics.s3.us-east-2.amazonaws.com/tokenizer.zip), [labelEncoder](https://yca-analytics.s3.us-east-2.amazonaws.com/labelEncoder.joblib), [LSTM model](https://yca-analytics.s3.us-east-2.amazonaws.com/model_lstm.zip), and [LSTM weights](https://yca-analytics.s3.us-east-2.amazonaws.com/model_lstm_weights.h5). 

The application demo can be seen here: [Demo](https://www.youtube.com/watch?v=BNPqXxj8aqg). This demo is on local server, as due to the large size of the files required, heroku is not able to support the application. However, this application can be easily replicated. Steps to replicate are given in readme.md file of GitHub repository. Moreover, since we are using paid technologies like AWS and Youtube API, we did not make this application publicly available.

## Steps to Replicate

1. Clone github repository 
    
        git clone https://github.com/EashanKaushik/youtube-comment-analysis.git
        
2. Install requirements.txt

        pip install -r requirements.txt
 
3. Setup AWS Buckets, create two S3 buckets, one with public access and, one with private access. 

4. Download the [tokenizer](https://yca-analytics.s3.us-east-2.amazonaws.com/tokenizer.zip), [labelEncoder](https://yca-analytics.s3.us-east-2.amazonaws.com/labelEncoder.joblib), [LSTM model](https://yca-analytics.s3.us-east-2.amazonaws.com/model_lstm.zip), and [LSTM weights](https://yca-analytics.s3.us-east-2.amazonaws.com/model_lstm_weights.h5) and store these files into the public S3 bucket. 

5. Setup a Ec2 instance in the same region as the two buckets, make sure you have IAM role attached to EC2 giving access to s3. ssh into your bucket and run following series of commands: 

        sudo apt-get update
        sudo apt-get install python3-pip
        mkdir -p build/python/lib/python/3.8/site-packages
        pip3 install paramiko -t system build/python/lib/python/3.8/site-packages
        cd build
        sudo apt install zip
        zip -r packageParamiko.zip
        curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
        unzip awscliv2.zip
        sudo ./aws/install
        aws s3 cp packageParamiko.zip s3://private-bucket-name # to store packageParamiko.zip to S3 bucket
        
6. Create a lambda instance in the same region as both buckets and EC2 instance, add a layer with Paramiko package which is stored in S3. Paste [this](https://github.com/EashanKaushik/youtube-comment-analysis/blob/main/analysis/data-scrapping/lambda.py) code in your lambda instance. Make sure you have IAM role with full access to S3 and EC2, basic lambda role. 

7. Make a YouTube API key from google developers console and paste this key in line #48 of your lambda function. 

8. create a .env file in comment_analysis folder with following contents

        SECRET_KEY='your-django-project-key'
        DATABASES_PASSWORD='heroku-database-password'
        AWS_ACCESS_KEY_ID='aws-access-key'
        AWS_SECRET_ACCESS_KEY='aws-secret-access-key'
        AWS_S3_BUCKET='private-bucket-name'
        AWS_PUBLIC_BUCKET='public-bucket-name'
 
9. Make django migrations to Database of your choice, we have used Heroku add on PostGre Database. 

        python manage.py makemigrations
        python manage.py migrate

10. Start your server and make requests. 
        
        python manage.py runserver
