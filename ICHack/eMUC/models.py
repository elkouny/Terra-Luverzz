from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Picture(models.Model):
    SEX_CHOICES = [('M','Male'), ('F', 'Female'),('m','Male'), ('f', 'Female')]
    photo_path = models.CharField(max_length= 200)
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    sex = models.CharField(max_length=1, choices= SEX_CHOICES)
    ethnicity = models.CharField(max_length=100)

class Person(models.Model):
    SEX_CHOICES = [('M','Male'), ('F', 'Female'), ('m','Male'), ('f', 'Female')]
    name = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    sex = models.CharField(max_length=15, choices= SEX_CHOICES)

    def __str__(self):
        return self.name



