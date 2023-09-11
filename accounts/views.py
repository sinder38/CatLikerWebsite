from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm
from .models import CustomUser


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def update_ranks():
    CustomUser.objects.annotate(points=Count('liked_cats') + Count('disliked_cats'))
    # todo finish this function

def profile(request, pk):
    pr = CustomUser.objects.get(id=pk)
    return render(request, 'users/profile.html', {'profile': pr})


def profile_list(request):
    if request.method == 'GET':
        all_users = CustomUser.objects.all()
        return render(request, 'users/profile_list.html', {'profiles': all_users})
