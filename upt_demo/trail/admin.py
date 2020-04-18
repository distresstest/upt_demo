from django.contrib import admin
from . models import Trail, Item, Location, Game, Action, Event, Context

# Register your models here.


class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_name', 'item_description')


class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'location_name', 'location_description', 'location_visit_event')


class TrailAdmin(admin.ModelAdmin):
    list_display = ('id', 'trail_name', 'trail_description', 'trail_mission', 'trail_total_items')


class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'game_name', 'game_mission', 'game_total_items')


class ActionAdmin(admin.ModelAdmin):
    list_display = ('id', 'action_name', 'action_event')


class ContextAdmin(admin.ModelAdmin):
    list_display = ('id', 'context_index', 'context_text', 'context_location')


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_name')


admin.site.register(Item, ItemAdmin)
admin.site.register(Location, LocationAdmin )
admin.site.register(Trail, TrailAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(Context, ContextAdmin)
admin.site.register(Event, EventAdmin)



