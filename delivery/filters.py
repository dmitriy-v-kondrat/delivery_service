from django_filters import rest_framework as filters
from geopy import distance

from delivery.models import Truck, Cargo


class DistanceFilter:
    """
    Utility class for filtering trucks based on their distance from a cargo point.

    Args:
        obj: The Cargo object for which trucks are being filtered.
        miles_to_cargo (int): The maximum distance in miles to consider a truck for filtering (default: 450).

    Attributes:
        cargo_point (tuple): The latitude and longitude of the cargo's pick-up location.
        miles_to_cargo (int): The maximum distance in miles to consider a truck for filtering.

    Methods:
        n_point(): Calculate the northernmost point within the given distance from the cargo.
        n_e_point(): Calculate the northeastern point within the given distance from the cargo.
        n_w_point(): Calculate the northwestern point within the given distance from the cargo.
        s_point(): Calculate the southernmost point within the given distance from the cargo.
        trucks_select(): Filter trucks based on their latitude and longitude within the specified region.
        __distance_less(distance_to_cargo): Check if the given distance is less than or equal to the maximum distance.
        __write_cargo(number, distance_to_cargo): Create a dictionary with truck number and distance.
        trucks_to_cargo(): Count the number of trucks within the specified distance from the cargo.
        all_trucks(): Get a list of trucks with their distances from the cargo.

    """

    def __init__(self, obj, miles_to_cargo=450):
        self.cargo_point = obj.pick_up.latitude, obj.pick_up.longitude
        self.miles_to_cargo = miles_to_cargo

    def n_point(self):
        """Calculate the northernmost point within the given distance from the cargo."""
        n_p = distance.distance(miles=self.miles_to_cargo).destination(self.cargo_point, bearing=0)
        if n_p.longitude == self.cargo_point[1]:
            return n_p
        else:
            return None

    def n_e_point(self):
        """Calculate the northeastern point within the given distance from the cargo."""
        return distance.distance(miles=self.miles_to_cargo).destination(self.n_point(), bearing=90)

    def n_w_point(self):
        """Calculate the northwestern point within the given distance from the cargo."""
        return distance.distance(miles=self.miles_to_cargo).destination(self.n_point(), bearing=270)

    def s_point(self):
        """Calculate the southernmost point within the given distance from the cargo."""
        s_p = distance.distance(miles=self.miles_to_cargo).destination(self.cargo_point, bearing=180)
        if s_p.longitude == self.cargo_point[1]:
            return s_p
        else:
            return None

    def trucks_select(self, all_trucks=None):
        """Filter trucks based on their latitude and longitude within the specified region."""
        if self.n_point() is None or self.s_point() is None or all_trucks:
            res = Truck.objects.only(
                    'number',
                    'location__zip_code',
                    'location__latitude',
                    'location__longitude').select_related()
        else:
            res = Truck.objects.only(
                    'location__zip_code',
                    'location__latitude',
                    'location__longitude').select_related().filter(location__latitude__lte=self.n_point().latitude,
                                                                   location__longitude__lte=self.n_e_point().longitude,
                                                                   location__longitude__gte=self.n_w_point().longitude,
                                                                   location__latitude__gte=self.s_point().latitude,
                                                                   )

        return res

    def __distance_less(self, distance_to_cargo):
        """Check if the given distance is less than or equal to the maximum distance."""
        return distance_to_cargo.__le__(self.miles_to_cargo)

    @staticmethod
    def __write_cargo(number, distance_to_cargo):
        """Create a dictionary with truck number and distance."""
        return {'truck number': number, 'distance': f'{distance_to_cargo:.2f} miles'}

    def trucks_to_cargo(self) -> int:
        """Count the number of trucks within the specified distance from the cargo."""
        trucks = 0
        trucks_queryset = self.trucks_select()
        for truck in trucks_queryset:
            truck_point = (truck.location.latitude, truck.location.longitude)
            distance_to_cargo = distance.distance(self.cargo_point, truck_point).miles
            if self.__distance_less(distance_to_cargo):
                trucks += 1
        return trucks

    def all_trucks(self) -> list:
        """Get a list of trucks with their distances from the cargo."""
        trucks = []

        trucks_queryset = self.trucks_select(all_trucks=True)
        for truck in trucks_queryset:
            truck_point = (truck.location.latitude, truck.location.longitude)
            distance_to_cargo = distance.distance(self.cargo_point, truck_point).miles
            trucks.append(self.__write_cargo(truck.number, distance_to_cargo))

        return trucks


class CargoFilter(filters.FilterSet, DistanceFilter):
    """
        FilterSet for Cargo objects with additional distance-based filtering.

        This FilterSet extends the functionality of DistanceFilter to filter Cargo objects based on weight and
        distance to nearby trucks.

        Attributes:
            weight_from (filters.NumberFilter): Filter Cargo objects by weight greater than or equal to this value.
            weight_up_to (filters.NumberFilter): Filter Cargo objects by weight less than or equal to this value.
            miles_to_trucks (filters.NumberFilter): Filter Cargo objects by distance to nearby trucks.

        Methods:
            get_miles_to_trucks(qs, field_name, value): Custom filter method to calculate the distance to nearby trucks
                for Cargo objects and filter them based on the given value.

        """

    weight_from = filters.NumberFilter(label='weight from', field_name='weight', lookup_expr='gte')
    weight_up_to = filters.NumberFilter(label='weight up to', field_name='weight', lookup_expr='lte')
    miles_to_trucks = filters.NumberFilter(label='<= miles to trucks', method='get_miles_to_trucks')

    class Meta:
        model = Cargo
        fields = ('weight_from', 'weight_up_to', 'miles_to_trucks')

    def get_miles_to_trucks(self, qs, field_name, value):
        """
        Custom filter method to calculate the distance to nearby trucks for Cargo objects and filter them
        based on the given value.

        Args:
            qs (QuerySet): The queryset containing Cargo objects.
            field_name (str): The name of the field to filter.
            value (str): The maximum distance in miles.

        Returns:
            QuerySet: Filtered queryset containing Cargo objects that meet the distance criteria.

        """
        qs_distinct = qs.filter().distinct('pick_up')
        self.miles_to_cargo = int(value)
        obj_list = []
        for obj in qs_distinct:
            self.cargo_point = (obj.pick_up.latitude, obj.pick_up.longitude)
            trucks = self.trucks_to_cargo()
            if trucks > 0:
                self.request.data[str(obj.pick_up)] = trucks
                obj_list.append(obj.pick_up)
        return qs.filter(pick_up__in=obj_list)
