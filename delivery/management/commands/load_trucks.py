
import random
import string

from django.core.management import BaseCommand
from django.db import connection

from delivery.models import Location, Truck


class Command(BaseCommand):
    """Checks instance in Truck.model if not exist adds objects"""
    def __init__(self):
        super().__init__()
        self.locations = Location.objects.only('zip_code')

    def handle(self, *args, **kwargs):
        self.stdout.write('Check Truck.model')
        if Truck.objects.exists():
            self.stdout.write('Trucks exist')
        else:
            trucks_list = []
            for _ in range(20):
                truck = Truck(number=f'{random.randint(1000, 9999)}{random.choice(string.ascii_uppercase)}',
                              carrying_capacity=random.randint(1, 1000),
                              location=random.choice(self.locations)
                              )

                trucks_list.append(truck)
            Truck.objects.bulk_create(trucks_list)
            self.stdout.write('Trucks created')
