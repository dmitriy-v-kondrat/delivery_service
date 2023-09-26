import random

from delivery.models import Location, Truck


def truck_location_update():
    """ Updating the location of all trucks."""
    trucks_list = []
    locations = Location.objects.only('zip_code')
    trucks = Truck.objects.only('location')
    for truck in trucks:
        truck.location = random.choice(locations)
        trucks_list.append(truck)
    Truck.objects.bulk_update(trucks_list, ['location'])
