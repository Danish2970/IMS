from django.contrib import admin
from .models import Location, Floor, Room, Item

admin.site.register(Location)
admin.site.register(Floor)
admin.site.register(Room)
admin.site.register(Item)