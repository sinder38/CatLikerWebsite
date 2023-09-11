from django.contrib import admin

from .forms import CatAdminForm
from .models import Cat


# Register your models here.


class CatAdmin(admin.ModelAdmin):
    add_form = CatAdminForm  # custom field to use in get form!
    ordering = ["points"]


admin.site.register(Cat, CatAdmin)
