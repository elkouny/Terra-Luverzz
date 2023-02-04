from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Person(models.Model):
    SEX_CHOICES = [('M','Male'), ('F', 'Female')]
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    sex = models.CharField(max_length=1, choices= SEX_CHOICES)
    ethnicity = models.CharField(max_length=100)
    height = models.DecimalField(null=True)
    weight = models.DecimalField(null=True)


