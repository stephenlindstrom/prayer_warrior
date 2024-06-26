from django.db.models.query import QuerySet
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


class IndexView(LoginRequiredMixin, generic.ListView):
    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)
    
    model = Item
    template_name = "app/index.html"
    login_url = reverse_lazy("login")


class DetailView(generic.DetailView):
    model = Item
    template_name = "app/detail.html"


class AddItemView(CreateView):
    model = Item
    fields = ["item_name"]
    template_name = "app/index.html"

# def add_item(request):
#     new_item = request.POST["item"]
#     Item.objects.create(item_name=new_item, user=request.user)
#     return redirect(reverse("app:index"))


class RegistrationView(SuccessMessageMixin, CreateView):
    template_name= "app/register.html"
    success_url = reverse_lazy("login")
    form_class = RegistrationForm
    success_message = "Your profile was created successfully"

