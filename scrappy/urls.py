from django.urls import path
from . import views

app_name = "scrappy"
urlpatterns = [
    path("", views.url_entry, name="url_entry"),
    path("request/", views.order_request, name="order_request"),
    path("analyze/<str:request_display>", views.analyze, name="analyze"),
    path("loading/<str:request_display>", views.loading, name="loading"),
]
