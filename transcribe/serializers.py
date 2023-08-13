from transcribe.models import Transcription

from rest_framework import serializers


class TranscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcription
        fields = (
            "email",
            "link",
            "language",
        )
