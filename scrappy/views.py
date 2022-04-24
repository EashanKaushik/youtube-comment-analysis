from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from .models import Request
from .driver import check_analyze

from comment_analysis.lambda_config import (
    update_request,
    trigger_lambda,
    read_analyzed_data,
)
from .predict_data import analyze_data

import secrets


def url_entry(request):

    if request.method == "POST" and "submit" in request.POST:

        url_request = Request()

        url_request.url = request.POST.get("url")

        url_request.save()

        request_id = secrets.token_urlsafe(int(url_request.request_id))

        if len(str(request_id)) > 7:
            request_id = request_id[0:6]

        url_request.request_display = request_id

        url_request.save()

        trigger_lambda(request.POST.get("url"), url_request.request_display)
        messages.success(request, "Order Submitted!!")

        context = {
            "page_name": "Scrap",
            "url_sent": True,
            "request_id": url_request.request_display,
        }

        return render(request, "scrappy/index.html", context)

    context = {
        "page_name": "Scrap",
        "url_sent": False,
    }
    return render(request, "scrappy/index.html", context)


def order_request(request):

    completed = False
    post = False
    request_id = None

    if request.method == "POST" and "submit" in request.POST:

        request_id = request.POST.get("request")

        try:
            update_request(request_id)
        except Exception:
            messages.error(request, "Request Pending!")

        try:
            completed = Request.objects.get(request_display=request_id).completed
        except Exception:
            messages.error(request, "Not a Valid Request ID!")

        if completed:
            request_id = request.POST.get("request")
            messages.success(request, "Data Scrapped!")

        post = True

    context = {
        "page_name": "Request",
        "completed": completed,
        "post": post,
        "request_id": request_id,
    }
    return render(request, "scrappy/request.html", context)


def loading(request, request_display):

    loading_page = False

    context = {
        "page_name": "Analyze",
        "loading_page": loading_page,
        "request_id": request_display,
    }
    return render(request, "scrappy/loading.html", context)


def analyze(request, request_display):

    if not check_analyze(request_display):
        analyze_data(request_id=request_display)

    try:
        data = read_analyzed_data(request_id=request_display)
        positive = data[data.Sentiment == "Positive"]
        negative = data[data.Sentiment == "Negative"]
        neutral = data[data.Sentiment == "Neutral"]

        positive_number = len(positive.index)
        negative_number = len(negative.index)
        neutral_number = len(neutral.index)

        positive = (
            positive_number / (positive_number + negative_number + neutral_number)
        ) * 100
        negative = (
            negative_number / (positive_number + negative_number + neutral_number)
        ) * 100
        neutral = (
            neutral_number / (positive_number + negative_number + neutral_number)
        ) * 100

    except Exception:
        messages.error(request, "Can't be Analyzed")

    context = {
        "page_name": "Analyze",
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
    }
    return render(request, "scrappy/analyze.html", context)
