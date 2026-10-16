from base.api.modules.hit_streak import longest_hit_streak
from base.models import Movie, MovieRun, Run, User
from django.conf import settings  # type: ignore
from django.test import SimpleTestCase, override_settings  # type: ignore
from django.urls import reverse  # type: ignore
from rest_framework.test import APIClient, APITestCase  # type: ignore


class LongestHitStreakTests(SimpleTestCase):
    def test_empty_list(self):
        self.assertEqual(longest_hit_streak([]), 0)

    def test_only_misses(self):
        self.assertEqual(longest_hit_streak([False, False, False]), 0)

    def test_streak_in_the_middle(self):
        self.assertEqual(longest_hit_streak([False, True, True, False]), 2)

    def test_single_hit_between_misses(self):
        self.assertEqual(longest_hit_streak([False, True, False]), 1)

    def test_longest_of_several_streaks(self):
        self.assertEqual(
            longest_hit_streak([True, True, True, False, True, True, False]), 3
        )
    
    def test_all_hits(self):
        self.assertEqual(longest_hit_streak([True, True, True]), 3)

    def test_earlier_streak_wins_over_a_later_shorter_one(self):
        self.assertEqual(longest_hit_streak([True, True, True, False, True]), 3)


# CreateAdminMiddleware recreates an "admin" user on every request; irrelevant here
MIDDLEWARE_WITHOUT_ADMIN = [
    m for m in settings.MIDDLEWARE if not m.endswith("CreateAdminMiddleware")
]


def make_movie(name):
    return Movie.objects.create(
        name=name,
        year=2000,
        director="Some Director",
        hints_amount=3,
        difficulty_level=3,
    )


@override_settings(MIDDLEWARE=MIDDLEWARE_WITHOUT_ADMIN)
class MyBestStreakViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="player", password="secret123")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("my_best_streak")
        self.movie = make_movie("Alien")

    def answer(self, user, outcomes):
        """outcomes is a list of 'hit', 'miss' or 'skip', played in this order"""
        run = Run.objects.create(user=user, movies_left=0, total_points=0)

        for outcome in outcomes:
            MovieRun.objects.create(
                run=run,
                original_movie=self.movie,
                has_hit=outcome == "hit",
                has_missed=outcome == "miss",
            )

    def test_requires_authentication(self):
        self.assertEqual(APIClient().get(self.url).status_code, 401)

    def test_no_answers(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"best_hit_streak": 0, "movies_answered": 0})

    def test_best_streak(self):
        self.answer(self.user, ["hit", "miss", "hit", "hit", "miss"])

        response = self.client.get(self.url)

        self.assertEqual(response.data["best_hit_streak"], 2)
        self.assertEqual(response.data["movies_answered"], 5)

    def test_unanswered_movies_are_ignored(self):
        self.answer(self.user, ["hit", "skip", "hit", "miss"])

        response = self.client.get(self.url)

        self.assertEqual(response.data["movies_answered"], 3)

    def test_ignores_other_users(self):
        other = User.objects.create_user(username="other", password="secret123")
        self.answer(other, ["hit", "hit", "hit", "miss"])
        self.answer(self.user, ["hit", "miss"])

        response = self.client.get(self.url)

        self.assertEqual(response.data["best_hit_streak"], 1)
        self.assertEqual(response.data["movies_answered"], 2)
        
    def test_different_creation_order(self):
        mr1 = MovieRun.objects.create(
            run=Run.objects.create(user=self.user, movies_left=0, total_points=0),
            original_movie=self.movie,
            has_hit=True,
            has_missed=False,
        )
        
        mr2 = MovieRun.objects.create(
            run=Run.objects.create(user=self.user, movies_left=0, total_points=0),
            original_movie=self.movie,
            has_hit=False,
            has_missed=True,
        )
        
        mr3 = MovieRun.objects.create(
            run=Run.objects.create(user=self.user, movies_left=0, total_points=0),
            original_movie=self.movie,
            has_hit=True,
            has_missed=False,
        )
        
        mr1.id = 1
        mr3.id = 2
        mr2.id = 3
        mr1.save()
        mr2.save()
        mr3.save()
    
        response = self.client.get(self.url)

        self.assertEqual(response.data["best_hit_streak"], 1)
        self.assertEqual(response.data["movies_answered"], 3)
