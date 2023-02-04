from django.contrib import admin

from .models import Picture, Person

@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ['age', 'sex', 'ethnicity']

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'sex']
