from base.api.modules.summary import average_points, hit_rate_percent
from base.models import Run, User
from django.conf import settings  # type: ignore
from django.test import SimpleTestCase, override_settings  # type: ignore
from django.urls import reverse  # type: ignore
from rest_framework.test import APIClient, APITestCase  # type: ignore


class HitRatePercentTests(SimpleTestCase):
    def test_nothing_played(self):
        self.assertEqual(hit_rate_percent(0, 0), 0)

    def test_all_hits(self):
        self.assertEqual(hit_rate_percent(10, 0), 100)

    def test_no_hits(self):
        self.assertEqual(hit_rate_percent(0, 5), 0)

    def test_exact_percentages(self):
        self.assertEqual(hit_rate_percent(3, 1), 75)
        self.assertEqual(hit_rate_percent(1, 1), 50)

    def test_rounds_down(self):
        self.assertEqual(hit_rate_percent(1, 2), 33)  # 33.33...

    def test_rounds_up(self):
        self.assertEqual(hit_rate_percent(2, 1), 67)  # 66.66...

    def test_halves_round_up(self):
        self.assertEqual(hit_rate_percent(7, 1), 88)  # 87.5


class AveragePointsTests(SimpleTestCase):
    def test_no_finished_runs(self):
        self.assertEqual(average_points(0.0, 0), 0.0)

    def test_average_has_two_decimals(self):
        self.assertEqual(average_points(100.0, 3), 33.33)

    def test_exact_average(self):
        self.assertEqual(average_points(90.0, 3), 30.0)


# CreateAdminMiddleware recreates an "admin" user on every request; irrelevant here
MIDDLEWARE_WITHOUT_ADMIN = [
    m for m in settings.MIDDLEWARE if not m.endswith("CreateAdminMiddleware")
]


@override_settings(MIDDLEWARE=MIDDLEWARE_WITHOUT_ADMIN)
class MySummaryViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="player", password="secret123", total_hits=3, total_misses=1
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("my_summary")

    def test_requires_authentication(self):
        self.assertEqual(APIClient().get(self.url).status_code, 401)

    def test_user_without_runs(self):
        user = User.objects.create_user(username="newbie", password="secret123")
        self.client.force_authenticate(user=user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["hit_rate_percent"], 0)
        self.assertEqual(response.data["runs_played"], 0)
        self.assertEqual(response.data["best_run_points"], 0.0)
        self.assertEqual(response.data["average_points_per_finished_run"], 0.0)

    def test_summary_numbers(self):
        Run.objects.create(user=self.user, movies_left=0, total_points=40.0)
        Run.objects.create(user=self.user, movies_left=0, total_points=20.0)
        Run.objects.create(user=self.user, movies_left=3, total_points=99.0)

        response = self.client.get(self.url)

        self.assertEqual(response.data["username"], "player")
        self.assertEqual(response.data["hit_rate_percent"], 75)
        self.assertEqual(response.data["runs_played"], 3)
        self.assertEqual(response.data["finished_runs"], 2)
        self.assertEqual(response.data["best_run_points"], 99.0)
        self.assertEqual(response.data["average_points_per_finished_run"], 30.0)

    def test_ignores_other_users_runs(self):
        other = User.objects.create_user(username="other", password="secret123")
        Run.objects.create(user=other, movies_left=0, total_points=500.0)
        Run.objects.create(user=self.user, movies_left=0, total_points=10.0)

        response = self.client.get(self.url)

        self.assertEqual(response.data["runs_played"], 1)
        self.assertEqual(response.data["best_run_points"], 10.0)
