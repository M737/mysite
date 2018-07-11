from django.db import models

# Create your models here.

class Img(models.Model):
    name = models.CharField(max_length=255, default='')
    img_url = models.ImageField(upload_to='img')

    def __str__(self):
        return  self.name