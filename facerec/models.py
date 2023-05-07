import cv2
import numpy as np
from django.db import models
from tensorflow.python.ops.image_ops_impl import ssim


# Create your models here.
class Child(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=8)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class MissingChild(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='missing_children')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class AvailableChildPhotos(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='available_photos')
    photo = models.ImageField(upload_to='available_children')

    def __str__(self):
        return f"{self.photo.name}"


