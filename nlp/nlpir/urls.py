from django.urls import path
from . import views
urlpatterns = [
    path("parse", views.parse, name="parse"),
    path("upload", views.upload_bayes_datafile, name="upload"),
    path("query", views.query_sentiment, name="query"),
]