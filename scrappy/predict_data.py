from .models import Request

import os
import environ
import boto3
import time

import pandas as pd
import numpy as np
from cleantext import clean
import nltk
import pickle
import joblib

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow import keras

from comment_analysis.lambda_config import upload_data, get_lstm_model, get_encoder, get_tokenizer

VOCAB = 102612
EMBEDDINGS = 100
MAXIMUM_LENTH = 2100


def analyze_data(request_id):

    # try:
    data = read_data(request_id=request_id)
    print('data read')

    X = clean_data(data)
    print('data cleaned')
    X_pad_tokens = get_tokens(X)
    print('data tokens')
    y_labels = lstm_predict(X_pad_tokens)
    print('got labels')
    upload_data(y_labels, request_id)
    print('data uploaded')
    request = Request.objects.get(request_display=request_id)
    request.analyze_completed = True
    request.save()
    print('req saved')

    # except Exception:
    #     pass

    print(y_labels)


def read_data(request_id):
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    )

    url = Request.objects.get(request_display=request_id).url

    response = s3_client.get_object(
        Bucket=os.environ["AWS_S3_BUCKET"], Key="comment_data/" + url + ".csv"
    )

    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    if status == 200:
        dataframe = pd.read_csv(response.get("Body"))
    else:
        raise Exception("No bucket")

    # print(dataframe)
    return dataframe


def lemmatize_text(text, w_tokenizer, lemmatizer):
    comment = " ".join([lemmatizer.lemmatize(w) for w in w_tokenizer.tokenize(text)])

    if len(comment.replace(" ", "")) > 0:
        return comment

    return None


def clean_data(data):
    data["Comment"] = data["Comment"].astype(str)

    w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
    lemmatizer = nltk.stem.WordNetLemmatizer()

    for index, comment in enumerate(data["Comment"]):
        data.loc[index, "Comment"] = clean(
            comment,
            fix_unicode=True,  # fix various unicode errors
            to_ascii=True,  # transliterate to closest ASCII representation
            lower=True,  # lowercase text
            no_line_breaks=False,  # fully strip line breaks as opposed to only normalizing them
            no_urls=True,  # replace all URLs with a special token
            no_emails=True,  # replace all email addresses with a special token
            no_phone_numbers=True,  # replace all phone numbers with a special token
            no_numbers=True,  # replace all numbers with a special token
            no_digits=True,  # replace all digits with a special token
            no_currency_symbols=True,  # replace all currency symbols with a special token
            no_punct=True,  # remove punctuations
            no_emoji=True,
            replace_with_punct="",  # instead of removing punctuations you may replace them
            replace_with_url="",
            replace_with_email="",
            replace_with_phone_number="",
            replace_with_number="",
            replace_with_digit="",
            replace_with_currency_symbol="",
            lang="en",  # set to 'de' for German special handling
        )

    data["Comment"] = data["Comment"].apply(
        lambda text: lemmatize_text(text, w_tokenizer, lemmatizer)
    )

    X = data["Comment"]
    X.dropna(inplace=True)
    return X


def get_tokens(X):
    # with open("scrappy/LSTM/tokenizer.pickle", "rb") as handle:
    #     tokenizer = pickle.load(handle)
    
    tokenizer = get_tokenizer("tokenizer.pickle")

    X_tokens = tokenizer.texts_to_sequences(X)
    X_pad_tokens = pad_sequences(X_tokens, maxlen=MAXIMUM_LENTH, padding="post")

    return X_pad_tokens


def lstm_predict(X_pad_tokens):

    # lstm = keras.models.load_model("scrappy/LSTM/model_lstm.h5")
    # encoder = joblib.load("scrappy/LSTM/labelEncoder.joblib")
    
    lstm = get_lstm_model("model_lstm")
    encoder = get_encoder("labelEncoder.joblib")
    
    y_predictions = lstm.predict(X_pad_tokens)

    y_label = encoder.inverse_transform(y_predictions)

    labels = pd.DataFrame({"Sentiment": y_label.ravel()})

    return labels
    # print(y_label)
    # np.save('scrappy/LSTM/y_label', y_label)
    # print(y_predictions)
