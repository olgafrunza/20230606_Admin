from rest_framework import serializers
from .models import Flight, Reservation, Passenger

class FlightSerializer(serializers.ModelSerializer):
    # reservation = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Flight
        fields = "__all__"

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = "__all__"

class PassengerSerializerReservation(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False)
    class Meta:
        model = Passenger
        fields = "__all__"
        extra_kwargs = {"first_name":{"required": False}, 
                        "last_name":{"required": False},
                        "id": {"read_only": False, "required": False}
                        }

class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    flight = serializers.StringRelatedField()
    flight_id = serializers.IntegerField()
    # passenger = serializers.StringRelatedField(many=True)
    passenger = PassengerSerializerReservation(many=True)
    class Meta:
        model = Reservation
        fields = "__all__"
        extra_kwargs = {"user" : {"read_only" : True}, 
                        "flight" : {"required" : True}}
    
    def create(self, validated_data):
        passenger_data = validated_data.pop("passenger")
        print(passenger_data)
        reservation = Reservation.objects.create(**validated_data)

        for item in passenger_data:
            id = item.get("id")
            print(id)
            print(item.values())
            if id:
                passenger = Passenger.objects.get(id=id)
            else:
                passenger = Passenger.objects.create(**item)

            reservation.passenger.add(passenger)
            reservation.save()

        return reservation

class StaffFlightSerializer(serializers.ModelSerializer):
    reservation = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Flight
        fields = "__all__"