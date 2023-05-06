from django.contrib import admin

# Register your models here.
from facerec import models

admin.site.register(models.MissingChild)
admin.site.register(models.AvailableChildPhotos)
