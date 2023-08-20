from django.urls import path
from transcribe.views import Transcribe

app_name = "transcriber"
urlpatterns = [
    path("v1/transcribe", Transcribe.as_view({"post": "create"}), name="transcribe"),
]
