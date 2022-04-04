from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

def url_entry(request):
    context={
        "page_name": "Scrap" 
    }
    return render(request, "scrappy/index.html", context)

def order_request(request):
    context={
        "page_name": "Request"
    }
    return render(request, "scrappy/request.html", context)