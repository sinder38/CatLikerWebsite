from django.urls import path

from . import views

urlpatterns = [
    path("", views.random_cat, name="random_cat"),
    path("no_cats", views.no_cats, name="no_cats"),
    path("<str:cat_id>", views.certain_cat, name="certain_cat"),
]
