from django.shortcuts import render,get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,PermissionRequiredMixin)
# Create your views here.
#Group Views.py
from django.urls import reverse
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,RedirectView
from groups.models import Group,GroupMember

class CreateGroup(LoginRequiredMixin,CreateView):
    fields=('name','description')
    model=Group

class SingleGroup(DetailView):
    model = Group

class ListGroups(ListView):
    model = Group
class JoinGroup(LoginRequiredMixin,RedirectView) :
    def get_redirect_url(self):
        return reverse("groups:single",kwargs={'slug':self.kwargs.get('slug')})
    def get(self,request,*args, **kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))
        try:
            GroupMember.objects.create(user=self.request.user,group=group)
        except IntegrityError:
            messages.warning(self.request,"You are already a member of this group")
        else:
            messages.success(self.request,"You are now a member of this group")

        return super().get(request,*args, **kwargs)    

class LeaveGroup(LoginRequiredMixin,RedirectView):
    def get_redirect_url(self):
        return reverse("groups:single",kwargs={'slug':self.kwargs.get('slug')})
    def get(self,reguest,*args, **kwargs):
        try:
            membership = GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get('slug')
            ).get()
        except GroupMember.DoesNotExist:
            messages.warning(self.request,"You are not a member of this group")
        else:
            membership.delete()
            messages.success(self.request,"You have successfully left the group")
        return super().get(request,*args, **kwargs)    
