from django.db import models


# data about cats: id, link to image, rank, points and etc
class Cat(models.Model):
    id = models.CharField(max_length=200, primary_key=True, help_text='Cat image id. example: eOLpJytrbsQ')
    creation_date = models.DateTimeField(auto_now_add=True)
    link = models.SlugField(max_length=800,
                            help_text='Image download link. example: https://unsplash.com/photos/eOLpJytrbsQ/download')
    # ranking
    # ranks will be updated every hour.
    rank = models.PositiveIntegerField(null=True, blank=True, help_text='current rank of the cat compared to others')
    points = models.IntegerField(default=0, help_text='are based on user likes and dislikes')


# data about cat requests from api
class CatRequest(models.Model):
    # id is used for tracking pages. it starts from 1 which is great
    # todo do smth if admin deletes catrequest
    creation_date = models.DateTimeField(auto_now_add=True, help_text='also can be used for tracking api responses')
    per_page = models.IntegerField(help_text='request size')
    page = models.PositiveIntegerField(help_text='request page')
    successful_additions = models.PositiveIntegerField(default=0,help_text='how many cats was added successfully')
