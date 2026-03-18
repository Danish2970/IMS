from django.db import models

CATEGORY_CHOICES = [
    ('furniture', 'Furniture'),
    ('electronics', 'Electronics'),
    ('stationary', 'Stationary'),
]

class Location(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Floor(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=100) # Is this named 'name' or 'floor_name'?

    def __str__(self):
        return f"{self.location.name} - {self.name}"

class Room(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=50)

    def __str__(self):
        return f"Room {self.room_number} (Floor {self.floor.name})"


class Item(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='items')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    item_name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    date_in = models.DateField(null=True, blank=True)
    date_out = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='items/', null=True, blank=True)