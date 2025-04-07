from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    depertment = models.CharField(max_length=100)

    def __str__(self):
        return self.username
