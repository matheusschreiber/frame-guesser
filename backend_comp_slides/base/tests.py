from django.test import TestCase
from django.test.client import Client
from .models import User, Slide, SlideImage
from django.urls import reverse
import tempfile
import base64


class SlideTests(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'
        }
        User.objects.create_user(**self.credentials)

        self.new_slide = {
            'prof_discipline': 'test discipline',
            'hints_amount': 3,
            'difficulty_level': 3
        }
        slide = Slide.objects.create(**self.new_slide)

        mock_image = tempfile.NamedTemporaryFile(suffix=".jpg").name

        self.new_slide_image_0 = {'hint_index': 0,
                                  'slide': slide, 'image': mock_image}
        self.new_slide_image_1 = {'hint_index': 1,
                                  'slide': slide, 'image': mock_image}
        self.new_slide_image_2 = {'hint_index': 2,
                                  'slide': slide, 'image': mock_image}

        SlideImage.objects.create(**self.new_slide_image_0)
        SlideImage.objects.create(**self.new_slide_image_1)
        SlideImage.objects.create(**self.new_slide_image_2)

    # TODO: change this test to use AUTH 2.0
    def test_user_unauthenticated_should_not_fetch_new_slide(self):
        """
        if credentials dont match for the user, dont fetch new slide
        """

        self.username = "testuser"
        self.password = "wrongpassword"

        self.basic_auth_header = {
            'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode(f'{self.username}:{self.password}'.encode('utf-8')).decode('utf-8')
        }

        response = self.client.get(
            reverse('no-run-random-slide'), **self.basic_auth_header, follow=True)
        self.assertEqual(response.status_code, 401)

    # TODO: change this test to use AUTH 2.0
    def test_user_authenticated_should_fetch_new_slide(self):
        """
        if credentials match for the user, fetch new slide 
        """

        self.username = "testuser"
        self.password = "secret"

        self.basic_auth_header = {
            'HTTP_AUTHORIZATION': 'Basic ' + base64.b64encode(f'{self.username}:{self.password}'.encode('utf-8')).decode('utf-8')
        }

        response = self.client.get(
            reverse('no-run-random-slide'), **self.basic_auth_header, follow=True)
        self.assertEqual(response.status_code, 200)
