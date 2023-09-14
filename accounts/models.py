from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from CatTopChart.models import Cat


class CustomUser(AbstractUser):
    disliked_cats = models.ManyToManyField(Cat, related_name='cat_disliked', blank=True)
    liked_cats = models.ManyToManyField(Cat, related_name='cat_liked', blank=True)
    rank = models.PositiveIntegerField(null=True, blank=True, help_text='current rank of the user compared to others')
    points = models.IntegerField(default=0, help_text='depends on nuber of rated cats')

    def __str__(self):
        return self.username
