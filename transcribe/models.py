import os
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import transaction

from transcribe.tasks import process_transcription_and_send_email


class TrackableModel(models.Model):
    added = models.DateTimeField(
        auto_now_add=True, editable=False, null=True, blank=True, db_index=True
    )
    last_modified = models.DateTimeField(
        auto_now=True, editable=False, null=True, blank=True, db_index=True
    )

    class Meta:
        abstract = True


class Transcription(TrackableModel):
    email = models.EmailField()
    link = models.URLField(max_length=2000)
    title = models.CharField(blank=True, null=True, max_length=2000)
    transcript = models.TextField(blank=True, null=True)
    language = models.CharField(blank=True, null=True, max_length=255)

    def __str__(self) -> str:
        return f"Transcript for email: {self.email}"


@receiver(post_save, sender=Transcription)
def transcribe_and_send_email(sender, instance: Transcription, created, **kwargs):
    transaction.on_commit(
        lambda: process_transcription_and_send_email.delay(instance.id)
    )
