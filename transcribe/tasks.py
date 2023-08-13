import os
import re
from django.template.loader import render_to_string
from django.conf import settings

from transcriber.celery import app
from transcribe.utils import (
    convert_audio_to_transcript,
    convert_link_to_audio,
    send_email,
)
from googletrans import Translator
from celery import shared_task


@shared_task()
def process_transcription_and_send_email(transcript_id):
    from transcribe.models import Transcription

    transcription = Transcription.objects.get(id=transcript_id)

    existing_transcript = Transcription.objects.filter(
        link=transcription.link, transcript__isnull=False
    ).exclude(id=transcription.id)

    if existing_transcript.exists():
        if existing_transcript[0].language == transcription.language:
            Transcription.objects.filter(id=transcript_id).update(
                transcript=existing_transcript[0].transcript,
                language=existing_transcript[0].language,
                title=existing_transcript[0].title,
            )
            text = existing_transcript[0].transcript
        else:
            translator = Translator()
            translation = translator.translate(
                existing_transcript[0].transcript, dest=transcription.language
            )
            text = translation.text

            Transcription.objects.filter(id=transcript_id).update(
                transcript=text,
                title=existing_transcript[0].title,
            )

        title = title = existing_transcript[0].title

    else:
        audio, title = convert_link_to_audio(transcription.link)
        transcript = convert_audio_to_transcript(audio)
        text = transcript.get("text")

        if transcription.language != "en":
            translator = Translator()
            translation = translator.translate(
                transcript.get("text"), dest=transcription.language
            )
            text = translation.text

        Transcription.objects.filter(id=transcript_id).update(
            transcript=text,
            title=title,
        )

    content = {
        "link": transcription.link,
        "title": title,
        "text": text,
        "language": settings.TRANSCRIPTION_LANGUAGES[transcription.language],
    }

    content_text = render_to_string(
        "email/email.txt",
        content,
    )
    content_html = render_to_string(
        "email/email.html",
        content,
    )

    send_email(
        transcription.email,
        f"Your transcription for {title} is Ready!",
        content_text,
        content_html,
    )

    cleaned_title = re.sub("[^A-Z_ 0-9]", "", title, 0, re.IGNORECASE)
    print(f"Title: {title}")
    print(f"Cleaned Title: {cleaned_title}")

    if os.path.exists(f"{cleaned_title}.mp4"):
        print("Audio found, its to be crushed instantly Sire!!")
        os.remove(f"{cleaned_title}.mp4")
    else:
        print("Audio doesnt exist")
