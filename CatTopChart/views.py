import json
from datetime import date

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
from requests import JSONDecodeError

from CatTopChart.models import Cat
from accounts.models import CustomUser
from .get_cats import get_images


# show cat corresponding to id
def certain_cat(request, cat_id):
    if request.method == 'GET':
        cat = get_object_or_404(Cat, id=cat_id)
        context = {'cat': cat}
        return render(request, 'certain_cat.html', context)
    elif request.method == "POST":
        user = get_object_or_404(CustomUser, pk=request.user.pk)
        cat = get_object_or_404(Cat, id=cat_id)

        like = request.POST.get("like") == "true"
        if like:
            user.liked_cats.add(cat)
        else:
            user.disliked_cats.add(cat)

        context = {'cat': cat}
        return render(request, 'certain_cat.html', context)


def no_cats(request):
    return render(request, 'no_cats.html')


def __add_new_cats():
    try:
        new_cats = get_images(query=settings.IMAGE_PROVIDER_QUERY,
                              api_url=settings.IMAGE_PROVIDER_URL,
                              access_key=settings.IMAGE_PROVIDER_KEY,
                              count=settings.IMAGE_REQUEST_QUANTITY,
                              save=True)
        if len(new_cats):
            for cat in new_cats:
                try:
                    Cat.objects.create(id=cat[0], link=cat[1])
                except Exception as e:
                    print("oops2", e)
        else:
            print("no cats added")  # todo log better
    except JSONDecodeError:
        print("API error")
        # return HttpResponse(status=503)
        # todo select exceptions and redirect to page explaining api problems
    except Exception as e:
        print("Unexpected error with get_images", e)
        # return HttpResponse(status=503)


# show random cat the user has not yet seen
def random_cat(request):
    if request.method == 'GET':
        all_cats = Cat.objects.all()
        try:
            user = CustomUser.objects.get(pk=request.user.pk)
            user_liked_cats = user.liked_cats.all()
            user_disliked_cats = user.disliked_cats.all()
            user_rated_cats = user_disliked_cats.union(user_liked_cats)
            cat_list = all_cats.difference(user_rated_cats)  # get unrated cats
            if len(cat_list) <= 1:  # if there are no unrated cats left
                __add_new_cats()
            unseen_cat = cat_list.first()
        except CustomUser.DoesNotExist:
            # if user is not logged in then display random cat
            unseen_cat = all_cats.order_by('?').first()  # get random cat

        if unseen_cat:
            # display cat to user
            return redirect(reverse("certain_cat", kwargs={"cat_id": unseen_cat.id}))
        else:
            # this is not supposed to happen. app normally should just request more cats
            # so the user is told that there are no cats available
            return redirect(reverse("no_cats"))