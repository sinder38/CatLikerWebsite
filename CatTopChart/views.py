from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
from requests import JSONDecodeError

from CatTopChart.models import Cat
from accounts.models import CustomUser
from .get_cats import get_images


def __add_new_cats():
    try:
        new_cats = get_images(query=settings.IMAGE_PROVIDER_QUERY,
                              api_url=settings.IMAGE_PROVIDER_URL,
                              access_key=settings.IMAGE_PROVIDER_KEY,
                              count=settings.IMAGE_REQUEST_QUANTITY,
                              save=True)
        l_new_cats = len(new_cats)
        if l_new_cats:
            print(f"Attempting to add {l_new_cats}...")
            counter = 0
            for cat in new_cats:
                try:
                    Cat.objects.create(id=cat[0], link=cat[1])
                    counter += 1
                except Exception as e:
                    print("cat creation error", e)
            print(f"{counter} cats was added successfully")
        else:
            print("no cats added")  # todo log better
    except JSONDecodeError:
        print("API error")
    except Exception as e:
        print("Unexpected error with get_images", e)


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
            cat.points += int(user.disliked_cats.contains(cat)) + 1
            user.disliked_cats.remove(cat)
        else:
            user.disliked_cats.add(cat)
            cat.points -= int(user.liked_cats.contains(cat)) + 1
            user.liked_cats.remove(cat)
        return redirect(reverse("random_cat"))  # continue the cycle


def no_cats(request):
    return render(request, 'no_cats.html')


# show random cat the user has not yet seen
def random_cat(request):
    if request.method == 'GET':
        all_cats = Cat.objects.all()
        try:
            user = CustomUser.objects.get(pk=request.user.pk)
            unseen_cats = Cat.objects.exclude(cat_disliked=user).exclude(cat_liked=user)  # unrated cats
            if len(unseen_cats) <= 1:  # if there are no unrated cats left
                __add_new_cats()
            # todo optimize this
            unseen_cat = unseen_cats.order_by('?').first()  # get unseen random cat
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


def cat_list(request):
    # TODO add cat sorting to get worst cats
    if request.method == 'GET':
        all_cats = Cat.objects.order_by("-points")
        # update cat ranks :/ will be moved to celery later
        update_ranks()
        return render(request, 'cat_list.html', {'cats': all_cats})


def update_ranks():
    # todo move this to celery later
    all_cats = Cat.objects.all()

    # this is probably a bad way to do this
    for cat in all_cats:
        cat.points = len(CustomUser.objects.exclude(liked_cats=cat).all()) - len(
            CustomUser.objects.exclude(disliked_cats=cat).all())
        cat.save()

    for rank, cat in enumerate(all_cats.order_by("-points"), start=1):
        cat.rank = rank
        cat.save()
