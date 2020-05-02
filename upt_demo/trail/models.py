from django.db import models
from django.contrib.auth.models import User


class Trail(models.Model):
    trail_name = models.CharField(max_length=120) # max_length = required
    trail_description = models.TextField(blank=True, null=True)
    trail_mission = models.CharField(max_length=75, default="This is a mission")
    trail_total_items = models.IntegerField(default=0) # CharField(max_length=75, default="This is a mission")
    # trail_image = models.ImageField(upload_to='location_images', blank=True)
    trail_start_location = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return self.trail_name


class Item(models.Model):
    item_name = models.CharField(max_length=40, default="Item")
    item_description = models.TextField(max_length=200, default="This is an item")
    item_alt = models.CharField(max_length=40, default="This is an item")
    item_image = models.ImageField(upload_to='location_images', blank=True)

    def __str__(self):
        return self.item_name


class Event(models.Model):
    event_name = models.CharField(max_length=50)
    event_trail = models.ForeignKey(Trail, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.event_name




class Game(models.Model):
    game_name = models.CharField(max_length=120)
    game_mission = models.TextField(blank=True, null=True)
    game_player = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    game_url = models.CharField(max_length=16)
    game_start = models.DateTimeField(auto_now_add=True)
    game_inventory = models.ManyToManyField(Item, blank=True)
    game_total_items = models.IntegerField(default=0)
    game_trail = models.ForeignKey(Trail, null=True, on_delete=models.SET_NULL)
    game_duration = models.DurationField(null=True)
    game_progress = models.IntegerField(default=0)
    game_status = models.CharField(default='Not Started', max_length=20)
    game_event_list = models.ManyToManyField(Event, blank=True)
    # game_actions = models.ManyToManyField(Action, blank=True)

    def __str__(self):
        return self.game_name


class Action(models.Model):
    ACTION_VERBS = [('TAKE', 'Take Item'), ('USE', 'Use Item')]
    action_name = models.CharField(default='NO_ACTION', max_length=30)
    action_event = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)
    action_verb = models.CharField(max_length=10, choices=ACTION_VERBS, default='1')
    action_item  = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.action_name


class Location(models.Model):
    location_name = models.CharField(max_length=120) # max_length = required
    location_description = models.TextField(blank=True, null=True)
    location_url = models.CharField(max_length=16, default="This is a URL")
    location_inventory = models.ManyToManyField(Item, blank=True)
    location_visit_event = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)
    location_image = models.ImageField(upload_to='location_images', blank=True)

    def __str__(self):
        return self.location_name


class Context(models.Model):
    context_index = models.IntegerField(default=0)
    context_text = models.TextField(blank=True, null=True)
    context_action = models.ManyToManyField(Action, blank=True)
    context_location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)
    context_enable_events = models.ManyToManyField(Event, blank=True)

    def __str__(self):
        return str(self.context_index)
