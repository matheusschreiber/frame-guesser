from base.models import Movie, User
from django.urls import reverse  # type: ignore
from rest_framework.test import APIClient, APITestCase  # type: ignore


def make_movie(name, hits, misses, difficulty=3):
    return Movie.objects.create(
        name=name,
        year=2000,
        director="Some Director",
        hints_amount=3,
        difficulty_level=difficulty,
        total_hits=hits,
        total_misses=misses,
    )


class MovieStatsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="secret123")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("list_movie_stats")

        make_movie("Easy One", hits=18, misses=2)      # 0.9
        make_movie("Medium One", hits=10, misses=10)   # 0.5
        make_movie("Hard One", hits=2, misses=18)      # 0.1
        make_movie("Barely Played", hits=1, misses=1)  # below default min_plays

    def test_requires_authentication(self):
        response = APIClient().get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_hardest_is_default_and_sorted_by_lowest_hit_rate(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        names = [m["name"] for m in response.data]
        self.assertEqual(names, ["Hard One", "Medium One", "Easy One"])

    def test_easiest_order(self):
        response = self.client.get(self.url, {"order": "easiest"})
        names = [m["name"] for m in response.data]
        self.assertEqual(names, ["Easy One", "Medium One", "Hard One"])

    def test_hit_rate_is_computed_and_rounded(self):
        make_movie("Thirds", hits=2, misses=4)  # 0.333
        response = self.client.get(self.url)
        thirds = next(m for m in response.data if m["name"] == "Thirds")
        self.assertEqual(thirds["hit_rate"], 0.333)
        self.assertEqual(thirds["plays"], 6)

    def test_excludes_movies_with_too_few_plays(self):
        response = self.client.get(self.url)
        names = [m["name"] for m in response.data]
        self.assertNotIn("Barely Played", names)

    def test_limit_is_respected(self):
        response = self.client.get(self.url, {"limit": 2})
        self.assertEqual(len(response.data), 2)

    def test_invalid_order_returns_400(self):
        response = self.client.get(self.url, {"order": "sideways"})
        self.assertEqual(response.status_code, 400)

    def test_non_integer_params_return_400(self):
        response = self.client.get(self.url, {"limit": "abc"})
        self.assertEqual(response.status_code, 400)
