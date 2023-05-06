from django.db import models


# Create your models here.

class MissingChild(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    current_age = models.IntegerField()
    gender = models.CharField(max_length=20)
    date_missing = models.DateField()
    photo = models.ImageField(upload_to='missing_children')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ChildPhoto(models.Model):
    child = models.ForeignKey(MissingChild, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='missing_children')
    age_at_photo = models.IntegerField()

    def __str__(self):
        return f"{self.child} at age {self.age_at_photo}"
