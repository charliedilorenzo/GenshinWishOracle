from django.contrib import admin
from . import models

admin.site.register(models.Profile)
admin.site.register(models.PrimogemRecord)
admin.site.register(models.PrimogemSnapshot)