from django.test import TestCase
from django.test.client import Client
from .models import User, Slide, SlideImage
from django.urls import reverse
import tempfile
import base64


class SlideTests(TestCase):

    # this runs multiple times (one for each test function declared below)
    # TODO: change to only run once (?)
    def setUp(self):

        self.username = "testuser"
        self.password = "secret"

        User.objects.create_user(**{
            'username': self.username,
            'password': self.password
        })

        basic_encoded = base64.b64encode(
            f'{self.username}:{self.password}'.encode('utf-8')).decode('utf-8')

        self.basic_auth_header = {
            'HTTP_AUTHORIZATION': 'Basic ' + basic_encoded
        }

        new_slide = {
            'prof_discipline': 'test discipline',
            'hints_amount': 3,
            'difficulty_level': 3
        }
        slide = Slide.objects.create(**new_slide)

        mock_image = tempfile.NamedTemporaryFile(suffix=".jpg").name

        new_slide_image_0 = {'hint_index': 0,
                             'slide': slide, 'image': mock_image}
        new_slide_image_1 = {'hint_index': 1,
                             'slide': slide, 'image': mock_image}
        new_slide_image_2 = {'hint_index': 2,
                             'slide': slide, 'image': mock_image}

        SlideImage.objects.create(**new_slide_image_0)
        SlideImage.objects.create(**new_slide_image_1)
        SlideImage.objects.create(**new_slide_image_2)

    def test_user_unauthenticated_should_not_fetch_new_slide(self):
        """
        if credentials dont match for the user, dont fetch new slide
        """
        basic_hashed = base64.b64encode(
            'wrongusername:wrongpassword'.encode('utf-8')).decode('utf-8')

        wrong_credentials_header = {
            'HTTP_AUTHORIZATION': 'Basic ' + basic_hashed}

        url = '/api/slide/random'
        response = self.client.get(
            url, **wrong_credentials_header, follow=True)

        self.assertEqual(response.status_code, 401)

    def test_user_authenticated_should_fetch_new_slide(self):
        """
        if credentials match for the user, fetch new slide 
        """

        url = '/api/slide/random'
        response = self.client.get(url, **self.basic_auth_header, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_user_authenticated_should_fetch_new_hint(self):
        """
        if credentials match for the user, fetch new hint (slide image)
        the id of the run is passed via params
        """

        response = self.client.get(
            '/api/slide/random', **self.basic_auth_header, follow=True)

        self.current_run_id = response.data['run_id']

        url = '/api/slide/hint/' + str(self.current_run_id)
        response = self.client.post(url, **self.basic_auth_header, follow=True)

        self.assertEqual(response.status_code, 200)
