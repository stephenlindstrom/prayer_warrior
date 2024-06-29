from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import PrayerRequest

class PrayerRequestModelTests(TestCase):
    def setUp(self):
        User.objects.create_user(username="testuser", password="y0lo5432")
        
    def test_prayer_request_content(self):
        user = User.objects.get(username="testuser")
        prayer_request = PrayerRequest(datetime=datetime.now(), user=user, content="prayer request", answered=True)
        self.assertIs(prayer_request.content, "prayer request")

    def test_prayer_request_user(self):
        user = User.objects.get(username="testuser")
        prayer_request = PrayerRequest(datetime=datetime.now(), user=user, content="prayer request", answered=True)
        self.assertIs(prayer_request.user, user)

    def test_prayer_request_datetime(self):
        user = User.objects.get(username="testuser")
        current_datetime= datetime.now()
        prayer_request = PrayerRequest(datetime=current_datetime, user=user, content="prayer request", answered=True)
        self.assertIs(prayer_request.datetime, current_datetime)

    def test_prayer_request_answered_default(self):
        user = User.objects.get(username="testuser")
        prayer_request = PrayerRequest(datetime=datetime.now(), user=user, content="prayer request")
        self.assertIs(prayer_request.answered, False)


class PersonalPrayerViewTests(TestCase):
    def setUp(self):
        User.objects.create_user(username="testuser", password="y0lo5432")
        User.objects.create_user(username="testuser2", password="y0lo6543")

    def test_user_not_logged_in(self):
        response = self.client.get(reverse("app:personal-prayer"))
        self.assertRedirects(response, "/login/?next=/app/personal-prayer/")
        response = self.client.get("/login/?next=/app/personal-prayer/")
        self.assertContains(response, "Please login to see this page.")

    def test_no_prayers(self):
        self.client.login(username="testuser", password="y0lo5432")
        response = self.client.get(reverse("app:personal-prayer"))
        self.assertTemplateUsed(response, template_name="app/personal-prayer.html")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No items")

    def test_one_prayer(self):
        self.client.login(username="testuser", password="y0lo5432")
        user = User.objects.get(username="testuser")
        PrayerRequest.objects.create(datetime=datetime.now(), user=user, content="prayer request")
        response = self.client.get(reverse("app:personal-prayer"))
        self.assertContains(response, "prayer request", status_code=200)

    def test_multiple_prayers_same_user(self):
        self.client.login(username="testuser", password="y0lo5432")
        user = User.objects.get(username="testuser")
        prayer_request1 = PrayerRequest.objects.create(datetime=datetime.now(), user=user, content="prayer request1")
        prayer_request2 = PrayerRequest.objects.create(datetime=datetime.now(), user=user, content="prayer request2")
        response = self.client.get(reverse("app:personal-prayer"))
        self.assertQuerySetEqual(list(response.context["prayer_request_list"]), [prayer_request1, prayer_request2])

    def test_multiple_prayers_different_users(self):
        self.client.login(username="testuser", password="y0lo5432")
        current_user = User.objects.get(username="testuser")
        user2 = User.objects.get(username="testuser2")
        prayer_request1 = PrayerRequest.objects.create(datetime=datetime.now(), user=current_user, content="prayer request1")
        prayer_request2 = PrayerRequest.objects.create(datetime=datetime.now(), user=user2, content="prayer request2")
        prayer_request3 = PrayerRequest.objects.create(datetime=datetime.now(), user=current_user, content="prayer request3")
        response = self.client.get(reverse("app:personal-prayer"))
        self.assertQuerySetEqual(list(response.context["prayer_request_list"]), [prayer_request1, prayer_request3])

class IndexViewTests(TestCase):
    def setUp(self):
        User.objects.create_user(username="testuser", password="y0lo5432")

    def test_user_not_logged_in(self):
        response = self.client.get(reverse("app:index"))
        self.assertRedirects(response, "/login/?next=/app/")
        response = self.client.get("/login/?next=/app/")
        self.assertContains(response, "Please login to see this page.")
    
    def test_user_logged_in(self):
        self.client.login(username="testuser", password="y0lo5432")
        response = self.client.get(reverse("app:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/index.html")


class RegistrationViewTests(TestCase):
    def test_successful_registration(self):
        username = "testuser"
        password1 = "y0lo5432"
        password2 = "y0lo5432"
        response = self.client.post(reverse("app:register"), {"username": username, "password1": password1, "password2": password2})
        self.assertRedirects(response, reverse("login"))