from django.db import models


# data about cats: id, link to image, rank, points and etc
class Cat(models.Model):
    id = models.CharField(max_length=200, primary_key=True, help_text='Cat image id. example: eOLpJytrbsQ')
    creation_date = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=800,
                            help_text='Image download link. example: https://unsplash.com/photos/eOLpJytrbsQ/download')
    # ranking
    # ranks will be updated every hour.
    rank = models.PositiveIntegerField(null=True, blank=True, help_text='current rank of the cat compared to others')
    points = models.IntegerField(default=0)
