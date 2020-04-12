from django.contrib import admin
from . models import Trail, Item, Location, Game

# Register your models here.


class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_name', 'item_description')


class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'location_name', 'location_description')


class TrailAdmin(admin.ModelAdmin):
    list_display = ('id', 'trail_name', 'trail_description', 'trail_mission', 'trail_total_items')


class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'game_name', 'game_mission', 'game_total_items')


admin.site.register(Item, ItemAdmin)
admin.site.register(Location,LocationAdmin )
admin.site.register(Trail, TrailAdmin)
admin.site.register(Game,GameAdmin)

