from django.urls import path

from delivery.views import TruckCreateView, CargoCreateView, CargoDestroyView, CargoDetailView, CargoListView, \
    CargoUpdateView, \
    TruckUpdateView

urlpatterns = [
    path('cargo-create/', CargoCreateView.as_view(), name='cargo_create'),
    path('cargo-list/', CargoListView.as_view(), name='cargo_list'),
    path('cargo-detail/<int:pk>/', CargoDetailView.as_view(), name='cargo_detail'),
    path('cargo-update/<int:pk>/', CargoUpdateView.as_view(), name='cargo_update'),
    path('cargo-destroy/<int:pk>/', CargoDestroyView.as_view(), name='cargo_destroy'),
    path('truck-create/', TruckCreateView.as_view(), name='truck_create'),
    path('truck-update/<int:pk>/', TruckUpdateView.as_view(), name='truck_update'),
]