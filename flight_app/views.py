from django.shortcuts import render
from .models import Flight, Reservation, Passenger
from .serializers import FlightSerializer, ReservationSerializer, PassengerSerializer, StaffFlightSerializer
from .permissions import IsAdminOrReadOnly

from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from datetime import date, datetime
from django.db.models import Q

from rest_framework.permissions import IsAuthenticated

# Create your views here.

class FlightView(ModelViewSet):
    queryset = Flight.objects.all()
    # queryset = Flight.objects.filter(date__gt="2023-05-24")
    serializer_class = FlightSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["date"]
    filterset_fields = ["airlines", "departure_city", "arrival_city", "date"]

    def get_serializer_class(self):
        serializer = super().get_serializer_class()

        id = self.kwargs.get("pk")
        # print(self.kwargs)

        if id and self.request.user.is_staff:
            serializer = StaffFlightSerializer
        
        return serializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        
        today = date.today()
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        
        # return Flight.objects.filter(date__gte=today)
        return queryset.filter(Q(date__gt=today) | Q(date=today, time__gt=time))

    # def get_queryset(self):
    #     if self.request.user.is_staff:
    #         return super().get_queryset()
        
    #     today = date.today()
    #     now = datetime.now()
    #     time = now.strftime("%H:%M:%S")
        
    #     # return Flight.objects.filter(date__gte=today)
    #     return Flight.objects.filter(Q(date__gt=today) | Q(date=today, time__gt=time))

class ReservationView(ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        
        return queryset.filter(user = self.request.user)

class PassengerView(ModelViewSet):
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
