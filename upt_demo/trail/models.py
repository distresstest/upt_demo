from django.db import models
#from game.models import Game
from django.contrib.auth.models import User

class Item(models.Model):
    item_name = models.CharField(max_length=40, default="Item")
    item_description = models.TextField(max_length=200, default="This is an item")
    # image = models.ImageField(upload_to='location_images', blank=True)


# class Inventory(models.Model):
#     inventory_item = models.ManyToManyField(Item, null=True, blank=True)
#     inventory_date_added = models.DateTimeField(auto_now_add=True, null=True)


class Game(models.Model):
    game_name = models.CharField(max_length=120) # max_length = required
    game_description = models.TextField(blank=True, null=True)
    game_player = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    game_url = models.CharField(max_length=16)
    game_start = models.DateTimeField(auto_now_add=True)
    game_inventory = models.ManyToManyField(Item, blank=True)
    #game_trail = models.ForeignKey(Trail, default="Trail X", on_delete=models.SET_DEFAULT)

class Trail(models.Model):
    trail_name = models.CharField(max_length=120) # max_length = required
    trail_description = models.TextField(blank=True, null=True)
    trail_url = models.URLField(max_length=16, default="This is a URL")
    # trail_image = models.ImageField(upload_to='location_images', blank=True)


class Location(models.Model):
    location_name = models.CharField(max_length=120) # max_length = required
    location_description = models.TextField(blank=True, null=True)
    #location_inventory = models.ForeignKey(Inventory, default=1, on_delete=models.SET_DEFAULT)
    location_url = models.URLField(max_length=16, default="This is a URL")
    #location_inventory = models.ManyToManyField(Item, null=True, blank=True)

    # image = models.ImageField(upload_to='location_images', blank=True)



#
# Do This
# class User(models.Model):
#     name = models.CharField(max_length=100)
#
#
# class Inventory(models.Model):
#    user = models.OneToOneField(User,on_delete=models.CASCADE)
#
# class Item(models.Model):
#     name =models.CharField(max_length=40)
#     description = models.TextField(max_length=200)
#     value = models.FloatField()
#     invetory =models.ForeignKey(Inventory,on_delete=models.CASCADE)
#
# https://stackoverflow.com/questions/51142123/django-designing-model-item-inventory-user