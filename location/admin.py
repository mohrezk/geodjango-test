from django.contrib import admin
from .models import Location

from django.contrib.gis.db import models
from django.contrib.gis.forms import OSMWidget


class Map(admin.ModelAdmin):
    formfield_overrides = {models.PointField: {"widget": OSMWidget}}


admin.site.register(Location, Map)
