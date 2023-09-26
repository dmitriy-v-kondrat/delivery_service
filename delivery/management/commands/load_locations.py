
import json

from django.core.management.base import BaseCommand
import csv

from django.db import connection

from delivery.models import Location


class Command(BaseCommand):
    """Checks objects in Location.model if not exist adds objects from csv-file."""

    def handle(self, *args, **kwargs):
        self.stdout.write('Check locations in db')
        if Location.objects.exists():
            self.stdout.write(self.style.SUCCESS('locations exist'))
        else:
            with open('uszips.csv', 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                json_file = json.dumps(list(reader)).replace("'", "`")

            sql_query = "INSERT INTO delivery_location (zip_code, city, state, latitude, longitude)" \
                        " SELECT zip, city, state_name, lat, lng FROM json_to_recordset ('"f'{json_file}'"')" \
                        " as x(zip text, lat float8, lng float8, city text, state_name text);"

            with connection.cursor() as cursor:
                cursor.execute(sql_query)
            self.stdout.write(self.style.SUCCESS('locations created'))
