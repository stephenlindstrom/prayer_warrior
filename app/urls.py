from django.urls import path

from . import views

app_name = "app"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("personal-prayer/", views.PersonalPrayerView.as_view(), name="personal-prayer"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("register/", views.RegistrationView.as_view(), name="register"),
]