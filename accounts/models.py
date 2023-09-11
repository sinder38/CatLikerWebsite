from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from CatTopChart.models import Cat


class CustomUser(AbstractUser):
    user = models.CharField(max_length=20)
    disliked_cats = models.ManyToManyField(Cat, related_name='cat_disliked', blank=True)
    liked_cats = models.ManyToManyField(Cat, related_name='cat_liked', blank=True)

    def __str__(self):
        return self.username

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         # todo understand manytomany rel in django
#         user_profile = Profile(user=instance)
#         user_profile.save()
#
#         user_profile.follows.set([instance.profile.id])
#         user_profile.save()


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     follows = models.ManyToManyField(
#         "self",
#         related_name="followed_by",
#         symmetrical=False,
#         blank=True)
#
#     def __str__(self):
#         return self.user.username
