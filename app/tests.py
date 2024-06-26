from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Item

class ItemModelTests(TestCase):
    def test_item_name(self):
        item = Item(item_name="test item")
        self.assertIs(item.item_name, "test item")


class ItemIndexViewTests(TestCase):
    def setUp(self):
        User.objects.create_user(username="testuser", password="y0lo5432")

    def test_user_not_logged_in(self):
        response = self.client.get(reverse("app:index"))
        self.assertRedirects(response, "/login/?next=/app/")

    def test_no_items(self):
        self.client.login(username="testuser", password="y0lo5432")
        response = self.client.get(reverse("app:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No items")
        self.assertQuerySetEqual(response.context["item_list"], [])

    def test_one_item(self):
        self.client.login(username="testuser", password="y0lo5432")
        user = User.objects.get(username="testuser")
        item = Item.objects.create(item_name="test item", user=user)
        response = self.client.get(reverse("app:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["item_list"], [item],)

    def test_two_items(self):
        self.client.login(username="testuser", password="y0lo5432")
        user = User.objects.get(username="testuser")
        item1 = Item.objects.create(item_name="test item 1", user=user)
        item2 = Item.objects.create(item_name="test item 1", user=user)
        response = self.client.get(reverse("app:index"))
        self.assertQuerySetEqual(list(response.context["item_list"]), [item1, item2],)


class RegistrationViewTests(TestCase):
    def test_successful_registration(self):
        username = "testuser"
        password1 = "y0lo5432"
        password2 = "y0lo5432"
        response = self.client.post(reverse("app:register"), {"username": username, "password1": password1, "password2": password2})
        self.assertRedirects(response, reverse("login"))