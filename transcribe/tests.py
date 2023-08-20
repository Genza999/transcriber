from http import HTTPStatus as http_status_code

from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase


class TranscriberTestCase(APITestCase):
    """Transcriber test cases."""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_invalid_link_for_transcription(self):
        """Test for invalid link sent for transcription."""
        data = {
            "email": "dkisekka@gmail.com",
            "link": "youtbsdvnaa",  # invalid link
            "language": "en",
        }
        response = self.client.post(
            reverse("transcriber:transcribe"),
            data=data,
        )

        self.assertEqual(response.status_code, http_status_code.BAD_REQUEST)
        self.assertEqual(response.data["link"][0], "Enter a valid URL.")

    def test_invalid_youtube_link_for_transcription(self):
        """Test for invalid youtube link sent for transcription."""
        data = {
            "email": "dkisekka@gmail.com",
            "link": "https://yygoogle.com",  # invalid youtube link
            "language": "en",
        }
        response = self.client.post(
            reverse("transcriber:transcribe"),
            data=data,
        )

        self.assertEqual(response.status_code, http_status_code.BAD_REQUEST)
        self.assertEqual(response.data["non_field_errors"][0], "Invalid Youtube URL")

    def test_invalid_email_to_send_transcription(self):
        """Test for invalid link sent for transcription."""
        data = {
            "email": "dkgmail.i",  # Invalid email address
            "link": "https://www.youtube.com/watch?v=gUyeQg46hdI",
            "language": "en",
        }
        response = self.client.post(
            reverse("transcriber:transcribe"),
            data=data,
        )

        self.assertEqual(response.status_code, http_status_code.BAD_REQUEST)
        self.assertEqual(response.data["email"][0], "Enter a valid email address.")
