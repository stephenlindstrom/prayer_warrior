from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, Http404
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView

from .forms import RegistrationForm
from .models import PrayerRequest

class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name="app/index.html"
    login_url = reverse_lazy("login")


class PersonalPrayerView(LoginRequiredMixin, generic.ListView):
    model = PrayerRequest
    login_url = reverse_lazy("login")
    template_name = "app/personal-prayer.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["prayer_request_list"] = self.model.objects.filter(user=self.request.user)
        return context


class AddPrayerRequestView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = PrayerRequest
    fields = ["content"]
    template_name = "app/prayer-request.html"
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("app:prayer-request")
    success_message = "Your request was successfully added."

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class RegistrationView(SuccessMessageMixin, CreateView):
    template_name= "app/register.html"
    success_url = reverse_lazy("login")
    form_class = RegistrationForm
    success_message = "Your profile was created successfully"


