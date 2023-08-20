import re
from rest_framework import serializers

from transcribe.models import Transcription

youtube_link_format = re.compile(
    r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|live\/|v\/)?)([\w\-]+)(\S+)?$"
)


class TranscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcription
        fields = (
            "email",
            "link",
            "language",
        )

    def validate(self, attrs):
        if not youtube_link_format.match(attrs.get("link")):
            raise serializers.ValidationError("Invalid Youtube URL")

        return super().validate(attrs)
