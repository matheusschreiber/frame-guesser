from base.models import Run, User
from django.conf import settings  # type: ignore
from django.test import override_settings  # type: ignore
from django.urls import reverse  # type: ignore
from rest_framework.test import APIClient, APITestCase  # type: ignore

# CreateAdminMiddleware recreates an "admin" user on every request; irrelevant here
MIDDLEWARE_WITHOUT_ADMIN = [
    m for m in settings.MIDDLEWARE if not m.endswith("CreateAdminMiddleware")
]


def make_run(user, movies_left, points=0.0):
    return Run.objects.create(user=user, movies_left=movies_left, total_points=points)


@override_settings(MIDDLEWARE=MIDDLEWARE_WITHOUT_ADMIN)
class MyRunsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="player", password="secret123")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("list_my_runs")

        self.finished_old = make_run(self.user, movies_left=0, points=42.5)
        self.in_progress = make_run(self.user, movies_left=4, points=10.0)
        self.finished_new = make_run(self.user, movies_left=0, points=77.123)

    def test_requires_authentication(self):
        self.assertEqual(APIClient().get(self.url).status_code, 401)

    def test_lists_all_runs_newest_first(self):
        response = self.client.get(self.url)
        ids = [r["id"] for r in response.data]
        self.assertEqual(ids, [self.finished_new.id, self.in_progress.id, self.finished_old.id])

    def test_run_fields(self):
        response = self.client.get(self.url)
        newest = response.data[0]
        self.assertEqual(newest["status"], "finished")
        self.assertEqual(newest["total_points"], 77.12)
        self.assertEqual(newest["movies_left"], 0)

    def test_filter_finished(self):
        response = self.client.get(self.url, {"status": "finished"})
        ids = {r["id"] for r in response.data}
        self.assertEqual(ids, {self.finished_old.id, self.finished_new.id})

    def test_filter_in_progress(self):
        response = self.client.get(self.url, {"status": "in_progress"})
        self.assertEqual([r["id"] for r in response.data], [self.in_progress.id])
        self.assertEqual(response.data[0]["status"], "in_progress")

    def test_does_not_list_other_users_in_progress_runs(self):
        other = User.objects.create_user(username="other", password="secret123")
        make_run(other, movies_left=3)
        response = self.client.get(self.url)
        self.assertEqual(len(response.data), 3)

    def test_limit(self):
        response = self.client.get(self.url, {"limit": 2})
        self.assertEqual(len(response.data), 2)

    def test_invalid_status_returns_400(self):
        self.assertEqual(self.client.get(self.url, {"status": "nope"}).status_code, 400)

    def test_invalid_limit_returns_400(self):
        self.assertEqual(self.client.get(self.url, {"limit": "x"}).status_code, 400)
        self.assertEqual(self.client.get(self.url, {"limit": 0}).status_code, 400)
