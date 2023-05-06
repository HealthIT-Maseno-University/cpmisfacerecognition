from django.db import models


# Create your models here.

class MissingChild(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='missing_children')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class AvailableChildPhotos(models.Model):
    photo = models.ImageField(upload_to='available_children')

    def __str__(self):
        return f"{self.photo.name}"
