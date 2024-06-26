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
from .models import Item

class IndexView(generic.TemplateView):
    template_name="app/index.html"


class PersonalPrayerView(LoginRequiredMixin, CreateView):
    model = Item
    fields = ["item_name"]
    template_name = "app/personal-prayer.html"
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("app:personal-prayer")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item_list"] = self.model.objects.filter(user=self.request.user)
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DetailView(generic.DetailView):
    model = Item
    template_name = "app/detail.html"


class RegistrationView(SuccessMessageMixin, CreateView):
    template_name= "app/register.html"
    success_url = reverse_lazy("login")
    form_class = RegistrationForm
    success_message = "Your profile was created successfully"

