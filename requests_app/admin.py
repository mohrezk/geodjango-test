from django.contrib import admin
from .models import Request
from django.contrib.gis.db import models
from django.contrib.gis.forms import OSMWidget
# Register your models here.

class Map(admin.ModelAdmin):
    formfield_overrides = {models.PointField: {"widget": OSMWidget}}

admin.site.register(Request,Map)
