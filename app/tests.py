from datetime import datetime
from django.contrib.auth.models import User, Group
from django.test import TestCase
from django.urls import reverse

from .models import AnsweredPrayer, PrayerRequest

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

    def test_answered_prayer(self):
        self.client.login(username="testuser", password="y0lo5432")
        user = User.objects.get(username="testuser")
        prayer_request1 = PrayerRequest.objects.create(datetime=datetime.now(), user=user, content="prayer request1", answered=True)
        prayer_request2 = PrayerRequest.objects.create(datetime=datetime.now(), user=user, content="prayer request2")
        response = self.client.get(reverse("app:personal-prayer"))
        self.assertQuerySetEqual(list(response.context["prayer_request_list"]), [prayer_request2])

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


class CreateGroupViewTests(TestCase):
    def setUp(self):
        User.objects.create_user(username="testuser", password="y0lo5432")

    def test_user_not_logged_in(self):
        response = self.client.get(reverse("app:create-group"))
        self.assertRedirects(response, "/login/?next=/app/create-group/")

    def test_successful_group_creation(self):
        self.client.login(username="testuser", password="y0lo5432")
        response = self.client.post(reverse("app:create-group"), {"name": "Test Group"})
        self.assertRedirects(response, reverse("app:create-group"))

    def test_current_user_in_new_group(self):
        user = User.objects.get(username="testuser")
        self.client.login(username="testuser", password="y0lo5432")
        self.client.post(reverse("app:create-group"), {"name": "Test Group"})
        self.assertTrue(user.groups.filter(name='Test Group').exists())


class AddMemberViewTests(TestCase):
    def setUp(self):
        User.objects.create_user(username="testuser", password="y0lo5432")
        User.objects.create_user(username="testuser2", password="y0lo4321")
        Group.objects.create(name="testgroup")

    def test_user_not_logged_in(self):
        response = self.client.get(reverse("app:add-member", kwargs={'group_id':1}))
        self.assertRedirects(response, "/login/?next=/app/group-prayers/1/add-member/")

    def test_user_not_member_of_group(self):
        self.client.login(username="testuser", password="y0lo5432")
        response = self.client.get(reverse("app:add-member", kwargs={'group_id':1}))
        self.assertEqual(response.status_code, 403)

    def test_get_user_member_of_group(self):
        self.client.login(username="testuser", password="y0lo5432")
        user = User.objects.get(username="testuser")
        group = Group.objects.get(name="testgroup")
        user.groups.add(group)
        response = self.client.get(reverse("app:add-member", kwargs={"group_id":1}))
        self.assertEqual(response.status_code, 200)
    
    def test_post_add_member(self):
        self.client.login(username="testuser", password="y0lo5432")
        user = User.objects.get(username="testuser")
        group = Group.objects.get(name="testgroup")
        user.groups.add(group)
        self.client.post(reverse("app:add-member", kwargs={"group_id":1}), {"username": "testuser2"})
        user2 = User.objects.get(username="testuser2")
        self.assertTrue(user2.groups.filter(name="testgroup").exists())

    def test_username_not_valid(self):
        self.client.login(username="testuser", password="y0lo5432")
        user = User.objects.get(username="testuser")
        group = Group.objects.get(name="testgroup")
        user.groups.add(group)
        response = self.client.post(reverse("app:add-member", kwargs={"group_id":1}), {"username": "testuser3"}, follow=True)
        self.assertRedirects(response, reverse("app:add-member", kwargs={"group_id":1}))
        self.assertContains(response, "Username does not exist")


class GroupListViewTests(TestCase):
    def setUp(self):
        User.objects.create_user(username="testuser", password="y0lo5432")
        User.objects.create_user(username="testuser2", password="y0lo4321")
        Group.objects.create(name="testgroup")
        Group.objects.create(name="testgroup2")
        Group.objects.create(name="testgroup3")

    def test_user_not_logged_in(self):
        response = self.client.get(reverse("app:group-prayers"))
        self.assertRedirects(response, "/login/?next=/app/group-prayers/")

    def test_user_not_in_any_groups(self):
        self.client.login(username="testuser", password="y0lo5432")
        response = self.client.get(reverse("app:group-prayers"))
        self.assertContains(response, "You do not belong to any groups")

    def test_user_in_one_group(self):
        self.client.login(username="testuser", password="y0lo5432")
        user = User.objects.get(username="testuser")
        group = Group.objects.get(name="testgroup")
        user.groups.add(group)
        response = self.client.get(reverse("app:group-prayers"))
        self.assertContains(response, group.name)

    def test_user_in_multiple_groups(self):
        self.client.login(username="testuser", password="y0lo5432")
        user = User.objects.get(username="testuser")
        group1 = Group.objects.get(name="testgroup")
        group2 = Group.objects.get(name="testgroup2")
        user.groups.add(group1)
        user.groups.add(group2)
        response = self.client.get(reverse("app:group-prayers"))
        self.assertQuerySetEqual(list(response.context["group_list"]), [group1, group2])
    
    def test_user_in_some_not_all_groups(self):
        self.client.login(username="testuser", password="y0lo5432")
        user1 = User.objects.get(username="testuser")
        user2 = User.objects.get(username="testuser2")
        group1 = Group.objects.get(name="testgroup")
        group2 = Group.objects.get(name="testgroup2")
        group3 = Group.objects.get(name="testgroup3")
        user1.groups.add(group1)
        user1.groups.add(group3)
        user2.groups.add(group2)
        response = self.client.get(reverse("app:group-prayers"))
        self.assertQuerySetEqual(list(response.context["group_list"]), [group1, group3])


class GroupDetailViewTests(TestCase):
    def setUp(self):
        User.objects.create_user(username="testuser", password="y0lo5432")
        User.objects.create_user(username="testuser2", password="y0lo4321")
        Group.objects.create(name="testgroup")
        Group.objects.create(name="testgroup2")
        Group.objects.create(name="testgroup3")
    
    def test_user_not_logged_in(self):
        response = self.client.get(reverse("app:group-detail", kwargs={"pk":1}))
        self.assertRedirects(response, "/login/?next=/app/group-prayers/1/")

    def test_user_not_in_group(self):
        self.client.login(username="testuser", password="y0lo5432")
        response = self.client.get(reverse("app:group-detail", kwargs={"pk":1}))
        self.assertEqual(response.status_code, 403)

    def test_user_in_group(self):
        self.client.login(username="testuser", password="y0lo5432")
        user = User.objects.get(username="testuser")
        group = Group.objects.get(name="testgroup")
        user.groups.add(group)
        response = self.client.get(reverse("app:group-detail", kwargs={"pk":1}))
        self.assertEqual(response.status_code, 200)


class PrayerRequestDeleteViewTests(TestCase):
    def setUp(self):
        User.objects.create_user(username="testuser", password="y0lo5432")
        User.objects.create_user(username="testuser2", password="y0lo4321")
        user = User.objects.get(username="testuser")
        user2 = User.objects.get(username="testuser2")
        PrayerRequest.objects.create(datetime=datetime.now(), user=user, content="prayer request")
        PrayerRequest.objects.create(datetime=datetime.now(), user=user2, content="prayer request 2")

    def test_user_not_logged_in(self):
        response = self.client.get(reverse("app:delete-prayer-request", kwargs={"pk":1}))
        self.assertRedirects(response, "/login/?next=/app/delete-prayer-request/1/")

    def test_unauthorized_user_get_request(self):
        self.client.login(username="testuser", password="y0lo5432")
        response = self.client.get(reverse("app:delete-prayer-request", kwargs={"pk":2}))
        self.assertEqual(response.status_code, 403)

    def test_successful_get_request(self):
        self.client.login(username="testuser", password="y0lo5432")
        response = self.client.get(reverse("app:delete-prayer-request", kwargs={"pk":1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/delete-prayer-request.html")

    def test_successful_post_request(self):
        self.client.login(username="testuser", password="y0lo5432")
        response = self.client.post(reverse("app:delete-prayer-request", kwargs={"pk":1}))
        self.assertRedirects(response, reverse("app:personal-prayer"))


class AddAnsweredPrayerViewTests(TestCase):
    def setUp(self):
        User.objects.create_user(username="testuser", password="y0lo5432")
        user = User.objects.get(username="testuser")
        PrayerRequest.objects.create(datetime=datetime.now(), user=user, content="prayer request", answered=False)
    
    def test_successful_post_add_answered_prayer(self):
        self.client.login(username="testuser", password="y0lo5432")
        response = self.client.post(reverse("app:add-answered-prayer", kwargs={"prayer_request_id": 1}), {"content": "answered"})
        self.assertRedirects(response, reverse("app:personal-prayer"))
        self.assertTrue(AnsweredPrayer.objects.filter(content="answered").exists())
        self.assertTrue(PrayerRequest.objects.filter(answered=True).exists())


class AnsweredPrayerListViewTests(TestCase):
    def setUp(self):
        User.objects.create_user(username="testuser", password="y0lo5432")
        user = User.objects.get(username="testuser")
        PrayerRequest.objects.create(datetime=datetime.now(), user=user, content="prayer request", answered=True)
        
    def test_user_not_logged_in(self):
        response = self.client.get(reverse("app:answered-prayer-list"))
        self.assertRedirects(response, "/login/?next=/app/answered-prayer-list/")

    def test_no_answered_prayers(self):
        self.client.login(username="testuser", password="y0lo5432")
        response = self.client.get(reverse("app:answered-prayer-list"))
        self.assertContains(response, "No answered prayers")

    def test_single_user_answered_prayers(self):
        self.client.login(username="testuser", password="y0lo5432")
        prayer_request = PrayerRequest.objects.get(content="prayer request")
        AnsweredPrayer.objects.create(datetime=datetime.now(), prayer_request=prayer_request, content="Answered prayer")
        answered_prayer = AnsweredPrayer.objects.get(content="Answered prayer")
        response = self.client.get(reverse("app:answered-prayer-list"))
        self.assertQuerySetEqual(list(response.context["answered_prayer_list"]), [answered_prayer]) 

    def test_multiple_users_answered_prayers(self):
        User.objects.create_user(username="testuser2", password="y0lo5432")
        user2 = User.objects.get(username="testuser2")
        PrayerRequest.objects.create(datetime=datetime.now(), user=user2, content="prayer request 2", answered=True)
        prayer_request = PrayerRequest.objects.get(content="prayer request")
        prayer_request2 =PrayerRequest.objects.get(content="prayer request 2")
        AnsweredPrayer.objects.create(datetime=datetime.now(), prayer_request=prayer_request, content="Answered prayer")
        AnsweredPrayer.objects.create(datetime=datetime.now(), prayer_request=prayer_request2, content="Answered prayer 2")
        answered_prayer = AnsweredPrayer.objects.get(content="Answered prayer")
        self.client.login(username="testuser", password="y0lo5432")
        response = self.client.get(reverse("app:answered-prayer-list"))
        self.assertQuerySetEqual(list(response.context["answered_prayer_list"]), [answered_prayer])