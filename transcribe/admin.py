from django.contrib import admin

from transcribe.models import Transcription

@admin.register(Transcription)
class TranscriptAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "link",)
    list_filter = (
        "id",
        "email",
    )
