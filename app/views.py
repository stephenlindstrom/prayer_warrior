from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User, Group
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView

from .forms import RegistrationForm, AddMemberForm
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


class CreateGroupView(LoginRequiredMixin, CreateView, SuccessMessageMixin):
    model = Group
    fields = ["name"]
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("app:create-group")
    template_name = "app/create-group.html"

    def form_valid(self, form):
        group = form.save()
        self.request.user.groups.add(group)
        return super().form_valid(form)
    

class GroupListView(LoginRequiredMixin, generic.ListView):
    


class AddMemberView(LoginRequiredMixin, UserPassesTestMixin, generic.FormView):
    login_url = reverse_lazy("login")
    template_name = "app/add-member.html"
    form_class = AddMemberForm

    def test_func(self):
        group_id = self.kwargs["group_id"]
        return self.request.user.groups.filter(id=group_id).exists()

    def get_success_url(self):
        group_id = self.kwargs["group_id"]
        return reverse_lazy("app:add-member", kwargs={"group_id":group_id})
    
    def form_valid(self, form):
        group_id = self.kwargs["group_id"]
        new_member_username = form.cleaned_data["username"]
        try:
            new_member = User.objects.get(username=new_member_username)
        except:
            messages.add_message(self.request, messages.ERROR, "Username does not exist")
            return redirect("app:add-member", group_id=group_id)
        group = Group.objects.get(id=group_id)
        new_member.groups.add(group)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group_id = self.kwargs["group_id"]
        context["group_id"] = group_id
        return context