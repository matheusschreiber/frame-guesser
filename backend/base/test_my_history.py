from datetime import timedelta

from base.models import Movie, MovieRun, Run, User
from django.urls import reverse  # type: ignore
from django.utils import timezone  # type: ignore
from rest_framework.test import APIClient, APITestCase  # type: ignore


def make_movie(name, year=2000):
    return Movie.objects.create(
        name=name,
        year=year,
        director="Some Director",
        hints_amount=3,
        difficulty_level=3,
    )


def make_run(user, days_back, movies, points=0.0):
    """movies is a list of (Movie, has_hit, hints_used, points) tuples"""
    run = Run.objects.create(user=user, movies_left=0, total_points=points)
    Run.objects.filter(pk=run.pk).update(
        created=timezone.now() - timedelta(days=days_back)
    )

    for movie, has_hit, hints_used, movie_points in movies:
        MovieRun.objects.create(
            run=run,
            original_movie=movie,
            has_hit=has_hit,
            has_missed=not has_hit,
            hints_used=hints_used,
            points=movie_points,
        )

    return run


class MyHistoryTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="player", password="secret123")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("list_my_history")

        self.alien = make_movie("Alien", 1979)
        self.heat = make_movie("Heat", 1995)
        self.up = make_movie("Up", 2009)

    def test_requires_authentication(self):
        self.assertEqual(APIClient().get(self.url).status_code, 401)

    def test_no_runs(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_lists_runs_newest_first_with_their_movies(self):
        old = make_run(self.user, 5, [(self.alien, True, 1, 8.0)], points=8.0)
        new = make_run(
            self.user,
            1,
            [(self.heat, True, 0, 10.0), (self.up, False, 3, 0.0)],
            points=10.0,
        )

        response = self.client.get(self.url)

        self.assertEqual([r["id"] for r in response.data], [new.id, old.id])

        newest = response.data[0]
        self.assertEqual(newest["total_points"], 10.0)
        self.assertEqual(newest["hits"], 1)
        self.assertEqual(
            [m["name"] for m in newest["movies"]],
            ["Heat", "Up"],
        )
        self.assertEqual(newest["movies"][1]["has_hit"], False)
        self.assertEqual(newest["movies"][1]["hints_used"], 3)

    def test_only_lists_my_runs(self):
        other = User.objects.create_user(username="other", password="secret123")
        make_run(other, 0, [(self.alien, True, 0, 10.0)])
        mine = make_run(self.user, 0, [(self.heat, True, 0, 10.0)])

        response = self.client.get(self.url)

        self.assertEqual([r["id"] for r in response.data], [mine.id])

    def test_limit(self):
        for days_back in range(5):
            make_run(self.user, days_back, [(self.alien, True, 0, 10.0)])

        response = self.client.get(self.url, {"limit": 2})

        self.assertEqual(len(response.data), 2)

    def test_limit_is_capped(self):
        response = self.client.get(self.url, {"limit": 500})

        self.assertEqual(response.status_code, 200)

    def test_invalid_limit_returns_400(self):
        self.assertEqual(self.client.get(self.url, {"limit": "x"}).status_code, 400)
        self.assertEqual(self.client.get(self.url, {"limit": 0}).status_code, 400)
