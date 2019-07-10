from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Image)
admin.site.register(models.Book)
admin.site.register(models.Page)
admin.site.register(models.Line)
admin.site.register(models.Character)
