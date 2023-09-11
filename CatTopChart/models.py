import random

from django.db import models
from django.db.models.aggregates import Count

# data about cats: id, link to image, rank, points and etc
class Cat(models.Model):
    id = models.CharField(max_length=200, primary_key=True, help_text='Cat image id. example: eOLpJytrbsQ')
    creation_date = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=800,
                            help_text='Image download link. example: http://unsplash.com/photos/eOLpJytrbsQ/download')
    # ranking
    # ranks will be updated every hour.
    rank = models.PositiveIntegerField(null=True,blank=True,help_text='current rank of the cat compared to others')
    points = models.IntegerField(default=0)

    # def save(self, *args, **kwargs):
    #     self.link = ("https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.wallpapers13.com%2Fwp-content"
    #                  "%2Fuploads%2F2016%2F01%2FCool-and-Beautiful-Nature-desktop-wallpaper-image-2560X1600-1600x1200"
    #                  ".jpg&f=1&nofb=1&ipt=7b2d828b28ccbfcaaa5068a8d106ff4401fc4abf76bcf610be9dd636e9a1670d&ipo=images")
    #     super(Cat, self).save(*args, **kwargs)

    # class Meta: # Cats going meta wtf
    #     ordering = ["points"]
    #     verbose_name_plural = "catz"
