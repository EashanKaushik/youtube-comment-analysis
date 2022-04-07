from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Request
from comment_analysis.lambda_config import update_request, trigger_lambda
import secrets
from django.contrib import messages

def url_entry(request):
    
    if request.method == 'POST' and 'submit' in request.POST:
        
        url_request = Request()
        
        url_request.url = request.POST.get("url")
        
        url_request.save()
        
        url_request.request_display = secrets.token_urlsafe(int(url_request.request_id))
        
        url_request.save()
        
        trigger_lambda(request.POST.get("url"), url_request.request_display)
        
        messages.success(request, "Order Submitted!!")
        
        context={
            "page_name": "Scrap",
            "url_sent": True,
            "request_id": url_request.request_display,
        }
        
        return render(request, "scrappy/index.html", context)
        
    context={
        "page_name": "Scrap",
        "url_sent": False,
    }
    return render(request, "scrappy/index.html", context)

def order_request(request):
    
    completed = False
    post = False
    
    if request.method == 'POST' and 'submit' in request.POST:
        
        request_id = request.POST.get("request")
        
        try: 
            update_request(request_id)
        except Exception:
            messages.error(request, "Request Pending!")
        
        completed = Request.objects.get(request_display=request_id).completed        
        
        if completed:
            messages.success(request, "Data Scrapped!")
        
        post = True
        
        
    
    context={
        "page_name": "Request",
        "completed": completed,
        "post": post,
    }
    return render(request, "scrappy/request.html", context)