from django.urls import path, include
from .views import SignUpView
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    #path("", home, name="home"),
    path("signup/", SignUpView.as_view(), name="signup"),
    # path("profile_list/", profile_list, name="profile_list"),
    # path("profile/<int:pk>", profile, name="profile")
]
