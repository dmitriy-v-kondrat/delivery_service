
import random
from rest_framework import serializers

from delivery.filters import DistanceFilter
from delivery.models import Truck, Cargo, Location


class CargoCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating Cargo instances.
    """

    pick_up = serializers.CharField(max_length=5, min_length=5, help_text='zip code')
    delivery = serializers.CharField(max_length=5, min_length=5, help_text='zip code')

    class Meta:
        model = Cargo
        fields = ('id', 'pick_up', 'delivery', 'weight', 'description')

    def validate_pick_up(self, value):
        if not Location.objects.filter(zip_code=value):
            message = 'Location matching query does not exist.'
            raise serializers.ValidationError([message])
        return value

    def validate_delivery(self, value):
        if not Location.objects.filter(zip_code=value):
            message = 'Location matching query does not exist.'
            raise serializers.ValidationError([message])
        return value

    def create(self, validated_data):
        query_bulk = Location.objects.in_bulk(id_list=[validated_data['pick_up'], validated_data['delivery']],
                                              field_name='zip_code'
                                              )
        instance = Cargo.objects.create(pick_up=query_bulk[validated_data['pick_up']],
                                        delivery=query_bulk[validated_data['delivery']],
                                        weight=validated_data['weight'],
                                        description=validated_data['description']
                                        )
        return instance


class CargoListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing Cargo instances with additional truck information.

    """

    def __init__(self, instance, **kwargs):
        super().__init__(instance, **kwargs)
        self.obj_dict = dict()

    trucks = serializers.SerializerMethodField()

    class Meta:
        model = Cargo
        fields = ('pk', 'pick_up', 'delivery', 'weight', 'description', 'trucks')

    def get_trucks(self, obj):

        if self.context['request'].GET.get('miles_to_trucks'):
            return self.context['request'].data.get(str(obj.pick_up))
        else:
            if str(obj.pick_up) not in self.obj_dict:
                trucks = DistanceFilter(obj).trucks_to_cargo()
                self.obj_dict.update({str(obj.pick_up): trucks})
                return trucks
            else:
                return self.obj_dict.get(str(obj.pick_up))


class CargoDetailSerializer(serializers.ModelSerializer):
    """
    Detailed information about a Cargo instance,
     including all trucks.
    """

    trucks = serializers.SerializerMethodField()

    class Meta:
        model = Cargo
        fields = ('pick_up', 'delivery', 'weight', 'description', 'trucks')

    def get_trucks(self, obj):
        return DistanceFilter(obj).all_trucks()


class CargoUpdateSerializer(serializers.ModelSerializer):
    """
    Cargo edit.

    """

    class Meta:
        model = Cargo
        fields = ('weight', 'description')


class CargoDestroySerializer(serializers.ModelSerializer):
    """
    Cargo delete.

    """

    class Meta:
        model = Cargo


class TruckCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new Truck instance.
    """
    carrying_capacity = serializers.IntegerField(min_value=1, max_value=1000)

    class Meta:
        model = Truck
        fields = ('number', 'carrying_capacity')

    def validate_number(self, value):
        """
       Validate the truck number.

       Args:
           value (str): The truck number to validate.

       Raises:
           serializers.ValidationError: If the truck number is not valid.

       Returns:
           str: The validated truck number.
       """
        if len(value) != 5:
            message = 'Must be 5'
            raise serializers.ValidationError([message])
        if not value[4].istitle():
            message = 'Must be capital letter'
            raise serializers.ValidationError([message])
        if not value[:4].isdigit():
            message = 'Must be digit'
            raise serializers.ValidationError([message])
        return value

    def create(self, validated_data):
        """
        Create a new Truck instance.

        Args:
            validated_data (dict): The validated data for creating a new Truck instance.

        Returns:
            Truck: The newly created Truck instance.
        """
        instance = Truck.objects.create(number=validated_data['number'],
                                        carrying_capacity=validated_data['carrying_capacity'],
                                        location=random.choice(Location.objects.all()),
                                        )
        return instance


class TruckUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating the location of a Truck instance.
    """
    class Meta:
        model = Truck
        fields = ('location',)
