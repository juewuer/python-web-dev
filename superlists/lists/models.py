from django.db import models

# Create your models here.

class List(models.Model):
    #note = models.TextField(default='')
    pass

class Item(models.Model):
    text = models.TextField(default='', blank=False)
    list = models.ForeignKey('List', on_delete = models.CASCADE, default=None)
