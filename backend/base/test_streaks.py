from datetime import date, timedelta, datetime

from base.api.modules.streaks import compute_streaks
from base.models import Run, User
from django.conf import settings  # type: ignore
from django.test import SimpleTestCase, override_settings  # type: ignore
from django.urls import reverse  # type: ignore
from django.utils import timezone  # type: ignore
from rest_framework.test import APIClient, APITestCase  # type: ignore

TODAY = date(2024, 3, 10)


def days_ago(*offsets):
    return [TODAY - timedelta(days=n) for n in offsets]


class ComputeStreaksTests(SimpleTestCase):
    def test_no_days_played(self):
        self.assertEqual(
            compute_streaks([], TODAY),
            {"current_streak": 0, "longest_streak": 0, "last_played": None},
        )

    def test_played_only_today(self):
        result = compute_streaks(days_ago(0), TODAY)

        self.assertEqual(result["current_streak"], 1)
        self.assertEqual(result["longest_streak"], 1)
        self.assertEqual(result["last_played"], TODAY)

    def test_consecutive_days_ending_today(self):
        result = compute_streaks(days_ago(2, 1, 0), TODAY)

        self.assertEqual(result["current_streak"], 3)
        self.assertEqual(result["longest_streak"], 3)

    def test_streak_is_still_alive_if_last_played_yesterday(self):
        result = compute_streaks(days_ago(3, 2, 1), TODAY)

        self.assertEqual(result["current_streak"], 3)

    def test_streak_is_lost_after_a_missed_day(self):
        result = compute_streaks(days_ago(4, 3, 2), TODAY)

        self.assertEqual(result["current_streak"], 0)
        self.assertEqual(result["longest_streak"], 3)

    def test_longest_streak_can_be_in_the_past(self):
        result = compute_streaks(days_ago(9, 8, 7, 6, 2, 1, 0), TODAY)

        self.assertEqual(result["current_streak"], 3)
        self.assertEqual(result["longest_streak"], 4)

    def test_days_do_not_need_to_be_sorted(self):
        result = compute_streaks(days_ago(0, 2, 1), TODAY)

        self.assertEqual(result["current_streak"], 3)
        self.assertEqual(result["longest_streak"], 3)

    def test_gap_of_one_day_breaks_the_streak(self):
        result = compute_streaks(days_ago(3, 1, 0), TODAY)

        self.assertEqual(result["current_streak"], 2)
        self.assertEqual(result["longest_streak"], 2)

    def test_streak_across_a_month_boundary(self):
        days = [date(2024, 2, 28), date(2024, 2, 29), date(2024, 3, 1)]

        self.assertEqual(compute_streaks(days, date(2024, 3, 1))["current_streak"], 3)
        
    def test_duplicate_dates(self):
        result = compute_streaks(days_ago(2, 1, 1, 0), TODAY)

        self.assertEqual(result["current_streak"], 3)
        self.assertEqual(result["longest_streak"], 3)


# CreateAdminMiddleware recreates an "admin" user on every request; irrelevant here
MIDDLEWARE_WITHOUT_ADMIN = [
    m for m in settings.MIDDLEWARE if not m.endswith("CreateAdminMiddleware")
]


@override_settings(MIDDLEWARE=MIDDLEWARE_WITHOUT_ADMIN)
class MyStreakViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="player", password="secret123")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("my_streak")

    def play(self, user, days_back):
        run = Run.objects.create(user=user, movies_left=0, total_points=0)
        moment = timezone.now() - timedelta(days=days_back)
        Run.objects.filter(pk=run.pk).update(created=moment)

    def test_requires_authentication(self):
        self.assertEqual(APIClient().get(self.url).status_code, 401)

    def test_no_runs(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["current_streak"], 0)
        self.assertEqual(response.data["last_played"], None)

    def test_streak_from_consecutive_days(self):
        for days_back in (2, 1, 0):
            self.play(self.user, days_back)

        response = self.client.get(self.url)

        self.assertEqual(response.data["current_streak"], 3)
        self.assertEqual(response.data["longest_streak"], 3)

    def test_ignores_other_users_runs(self):
        other = User.objects.create_user(username="other", password="secret123")
        for days_back in (2, 1, 0):
            self.play(other, days_back)
        self.play(self.user, 0)

        response = self.client.get(self.url)

        self.assertEqual(response.data["current_streak"], 1)
