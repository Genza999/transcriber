import logging

import whisper
from pytube import YouTube
from django.core.mail import EmailMultiAlternatives

from django.conf import settings

logger = logging.getLogger(__name__)


def convert_link_to_audio(link):
    youtube_object = YouTube(link).streams.filter(only_audio=True).first()
    if youtube_object:
        audio = youtube_object.download()
        return audio, youtube_object.title
    else:
        return None, None


def convert_audio_to_transcript(audio):
    model = whisper.load_model("base")
    transcript = model.transcribe(audio, fp16=False)
    return transcript


def send_email(recipient_email, subject, content, html_content):
    try:
        msg = EmailMultiAlternatives(
            # title:
            subject,
            # message:
            content,
            # from:
            settings.EMAIL_HOST_USER,
            # to:
            [recipient_email],
        )

        msg.attach_alternative(html_content, "text/html")
        # send the email
        msg.send()
    except Exception:
        logger.exception("EXCEPTION SENDING EMAIL.")
        raise
