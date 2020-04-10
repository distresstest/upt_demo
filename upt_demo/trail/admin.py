from django.contrib import admin
from . models import Trail, Item, Location, Game

# Register your models here.


class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'item_name', 'item_description')
admin.site.register(Item, ItemAdmin)

admin.site.register(Trail)
admin.site.register(Location)
admin.site.register(Game)


