from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register("flight", FlightView)
router.register("reservation", ReservationView)
router.register("passenger", PassengerView)

urlpatterns = [
    
] + router.urls
