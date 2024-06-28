from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Item

class ItemModelTests(TestCase):
    def test_item_name(self):
        item = Item(item_name="test item")
        self.assertIs(item.item_name, "test item")


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
        Item.objects.create(item_name="prayer", user=user)
        response = self.client.get(reverse("app:personal-prayer"))
        self.assertContains(response, "prayer", status_code=200)

    def test_multiple_prayers_same_user(self):
        self.client.login(username="testuser", password="y0lo5432")
        user = User.objects.get(username="testuser")
        prayer1 = Item.objects.create(item_name="prayer1", user=user)
        prayer2 = Item.objects.create(item_name="prayer2", user=user)
        response = self.client.get(reverse("app:personal-prayer"))
        self.assertQuerySetEqual(list(response.context["item_list"]), [prayer1, prayer2])

    def test_multiple_prayers_different_users(self):
        self.client.login(username="testuser", password="y0lo5432")
        current_user = User.objects.get(username="testuser")
        user2 = User.objects.get(username="testuser2")
        prayer1 = Item.objects.create(item_name="prayer1", user=current_user)
        prayer2 = Item.objects.create(item_name="prayer2", user=user2)
        prayer3 = Item.objects.create(item_name="prayer2", user=current_user)
        response = self.client.get(reverse("app:personal-prayer"))
        self.assertQuerySetEqual(list(response.context["item_list"]), [prayer1, prayer3])

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