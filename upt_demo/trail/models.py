from django.db import models

# Create your models here.


class Trail(models.Model):
    trail_name = models.CharField(max_length=120) # max_length = required
    trail_description = models.TextField(blank=True, null=True)
    # trail_image = models.ImageField(upload_to='location_images', blank=True)

class Location(models.Model):
    location_name = models.CharField(max_length=120) # max_length = required
    location_description = models.TextField(blank=True, null=True)
    # image = models.ImageField(upload_to='location_images', blank=True)

class Item(models.Model):
    item_name = models.CharField(max_length=120) # max_length = required
    item_description = models.TextField(blank=True, null=True)
    # image = models.ImageField(upload_to='location_images', blank=True)