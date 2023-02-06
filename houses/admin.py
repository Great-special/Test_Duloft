from django.contrib import admin

from .models import HouseModel, FlatModel, SpaceModel

# Register your models here.

admin.site.register([HouseModel, FlatModel, SpaceModel])