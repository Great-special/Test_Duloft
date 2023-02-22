from django.contrib import admin

from .models import HouseModel, FlatModel, SpaceModel, AmenitiesModels

# Register your models here.

admin.site.register([AmenitiesModels, HouseModel, FlatModel, SpaceModel])