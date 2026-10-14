from base.models import User
from django.conf import settings  # type: ignore
from django.test import override_settings  # type: ignore
from django.urls import reverse  # type: ignore
from rest_framework.test import APITestCase  # type: ignore


def make_user(name, points, hits=0, misses=0):
    return User.objects.create_user(
        username=name,
        password="secret123",
        total_points=points,
        total_hits=hits,
        total_misses=misses,
    )


# CreateAdminMiddleware recreates an "admin" user on every request, which would pollute the leaderboard
MIDDLEWARE_WITHOUT_ADMIN = [
    m for m in settings.MIDDLEWARE if not m.endswith("CreateAdminMiddleware")
]


@override_settings(MIDDLEWARE=MIDDLEWARE_WITHOUT_ADMIN)
class LeaderboardTests(APITestCase):
    def setUp(self):
        User.objects.all().delete()
        self.url = reverse("leaderboard")
        make_user("alice", 50, hits=5, misses=5)
        make_user("bob", 90, hits=9, misses=1)
        make_user("carol", 70, hits=7, misses=3)
        make_user("dave", 10)
        make_user("erin", 30, hits=1, misses=2)

    def test_is_public(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_orders_by_points_descending(self):
        response = self.client.get(self.url)
        names = [r["username"] for r in response.data["results"]]
        self.assertEqual(names, ["bob", "carol", "alice", "erin", "dave"])

    def test_first_page_ranks(self):
        response = self.client.get(self.url, {"page_size": 2})
        ranks = [(r["rank"], r["username"]) for r in response.data["results"]]
        self.assertEqual(ranks, [(1, "bob"), (2, "carol")])

    def test_second_page_has_the_next_players(self):
        response = self.client.get(self.url, {"page": 2, "page_size": 2})
        names = [r["username"] for r in response.data["results"]]
        self.assertEqual(names, ["alice", "erin"])

    def test_pagination_metadata(self):
        response = self.client.get(self.url, {"page_size": 2})
        self.assertEqual(response.data["total"], 5)
        self.assertEqual(response.data["total_pages"], 3)
        self.assertEqual(response.data["page"], 1)

    def test_page_past_the_end_is_empty(self):
        response = self.client.get(self.url, {"page": 10})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["results"], [])

    def test_ties_are_broken_by_username(self):
        make_user("aaron", 70)
        response = self.client.get(self.url)
        names = [r["username"] for r in response.data["results"]]
        self.assertEqual(names[1:3], ["aaron", "carol"])

    def test_accuracy(self):
        response = self.client.get(self.url)
        by_name = {r["username"]: r["accuracy"] for r in response.data["results"]}
        self.assertEqual(by_name["bob"], 0.9)
        self.assertEqual(by_name["erin"], 0.333)

    def test_accuracy_is_zero_without_attempts(self):
        response = self.client.get(self.url)
        by_name = {r["username"]: r["accuracy"] for r in response.data["results"]}
        self.assertEqual(by_name["dave"], 0.0)

    def test_page_size_is_capped(self):
        response = self.client.get(self.url, {"page_size": 500})
        self.assertEqual(response.data["page_size"], 50)

    def test_invalid_params_return_400(self):
        self.assertEqual(self.client.get(self.url, {"page": "x"}).status_code, 400)
        self.assertEqual(self.client.get(self.url, {"page": 0}).status_code, 400)
