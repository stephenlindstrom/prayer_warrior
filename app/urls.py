from django.urls import path

from . import views

app_name = "app"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("personal-prayer/", views.PersonalPrayerView.as_view(), name="personal-prayer"),
    path("register/", views.RegistrationView.as_view(), name="register"),
    path("prayer-request/", views.AddPrayerRequestView.as_view(), name="prayer-request"),
    path("create-group/", views.CreateGroupView.as_view(), name="create-group"),
    path("group-prayers/", views.GroupListView.as_view(), name="group-prayers"),
    path("group-prayers/<pk>/", views.GroupDetailView.as_view(), name="group-detail"),
    path("group-prayers/<int:group_id>/add-member/", views.AddMemberView.as_view(), name="add-member"),
]