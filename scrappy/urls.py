from django.urls import path
from . import views

app_name = "scrappy"
urlpatterns = [
    path("", views.url_entry, name="url_entry"),
]