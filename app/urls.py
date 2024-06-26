from django.urls import path

from . import views

app_name = "app"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("add_item/", views.AddItemView.as_view(), name="add_item"),
    path("register/", views.RegistrationView.as_view(), name="register"),
]