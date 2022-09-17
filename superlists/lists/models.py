from django.db import models
from django.shortcuts import reverse


# Create your models here.

class List(models.Model):
    def get_absolute_url(self):
        print(f'Get get_absolute_url {self}')
        ret = reverse('view_list', args=[self.id])
        print(f'Get get_absolute_ur {ret = }')
        return ret


class Item(models.Model):
    text = models.TextField(blank=False)
    list = models.ForeignKey('List', on_delete=models.CASCADE, default=None)
