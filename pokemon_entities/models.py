from django.db import models

# your models here


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
