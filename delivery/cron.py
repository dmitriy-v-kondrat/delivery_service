import random

from delivery.models import Location, Truck


def truck_location_update():
    for obj in Truck.objects.only('location'):
        obj.location = random.choice(Location.objects.all())
        obj.save(update_fields=['location'])
