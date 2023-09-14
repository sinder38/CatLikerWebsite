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
    # todo move this to celery later
    all_users = CustomUser.objects.all()
    for user in all_users:
        user.points = user.liked_cats.count()
        user.save()

    for rank, user in enumerate(all_users.order_by("-points"), start=1):
        user.rank = rank
        user.save()


def profile(request, pk):
    pr = CustomUser.objects.get(id=pk)
    return render(request, 'users/profile.html', {'profile': pr})


def profile_list(request):
    if request.method == 'GET':
        all_users = CustomUser.objects.order_by("-points")
        # update user ranks :/ will be moved to celery later
        update_ranks()
        return render(request, 'users/profile_list.html', {'profiles': all_users})
