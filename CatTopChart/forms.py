import random

from django import forms
from django.conf import settings
from django.forms import Textarea, IntegerField, formset_factory

from .models import Cat


class CatAdminForm(forms.ModelForm):
    class Meta:
        model = Cat
        fields = ["id", "link", "points"]

    def clean(self):
        super().clean()
        print("attempting overwrite")
        self.save(commit=False)
        self.cleaned_data['rank'] = random.randint(1, 100)
        self.save()
