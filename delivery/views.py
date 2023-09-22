
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from delivery.filters import CargoFilter
from delivery.models import Truck, Cargo
from delivery.serializers import CargoCreateSerializer, CargoDestroySerializer, \
    CargoDetailSerializer, CargoListSerializer, \
    CargoUpdateSerializer, TruckCreateSerializer, TruckUpdateSerializer


class CargoCreateView(generics.CreateAPIView):
    """
    Cargo create.
    """
    serializer_class = CargoCreateSerializer
    queryset = Cargo.objects.all()


class CargoListView(generics.ListAPIView):
    """
    Cargo list with quantity trucks. Default distance to trucks 450 miles.
    """
    queryset = Cargo.objects.select_related()
    serializer_class = CargoListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CargoFilter


class CargoDetailView(generics.RetrieveAPIView):
    """
    Obtaining information about a specific cargo.
    List of numbers of ALL vehicles with distance to the selected load.
    """
    queryset = Cargo.objects.select_related()
    serializer_class = CargoDetailSerializer


class CargoUpdateView(generics.UpdateAPIView):
    """
    Cargo edit.
    """
    queryset = Cargo.objects.all()
    serializer_class = CargoUpdateSerializer


class CargoDestroyView(generics.DestroyAPIView):
    """
    Cargo delete.
    """
    queryset = Cargo.objects.all()
    serializer_class = CargoDestroySerializer


class TruckCreateView(generics.CreateAPIView):
    """
    Truck create. Location choice random.
    """
    queryset = Truck.objects.all()
    serializer_class = TruckCreateSerializer


class TruckUpdateView(generics.UpdateAPIView):
    """
    Truck edit.
    """
    queryset = Truck.objects.all()
    serializer_class = TruckUpdateSerializer
