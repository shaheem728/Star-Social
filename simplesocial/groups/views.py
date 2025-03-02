from django.shortcuts import render
from django.contrib.auth.mixins import (LoginRequiredMixin,PermissionRequiredMixin)
# Create your views here.
from django.urls import reverse
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from groups.models import Group,GroupMember

class CreateGroup(LoginRequiredMixin,CreateView):
    fields=('name','description')
    model=Group

class SingleGroup(DetailView):
    model = Group

class ListGroups(ListView):
    model = Group