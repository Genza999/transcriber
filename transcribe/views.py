from django.shortcuts import render


from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin

from transcribe.serializers import TranscribeSerializer


def index(request):
    return render(request, "index.html")


class Transcribe(CreateModelMixin, GenericViewSet):
    serializer_class = TranscribeSerializer
    permission_classes = ()
