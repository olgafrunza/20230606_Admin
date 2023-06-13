from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from dj_rest_auth.serializers import TokenSerializer

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only = True, required=True)
    class Meta:
        model = User
        # fields = ("id", "username", "password", "password2", "first_name", "last_name", "email")
        fields = ("id", "password", "password2", "first_name", "last_name", "email")
        extra_kwargs = {"password" : {"write_only" : True, "validators": [validate_password]}, 
                        "email": {"required": True, "validators" : [UniqueValidator(User.objects.all())]}
                        }

    # runs after serializer.save() method and creates a record in database
    def create(self, validated_data):
        # user = User.objects.create(**validated_data)
        password = validated_data.pop("password")
        validated_data.pop("password2")
        user = User(**validated_data)
        user.username = user.email
        user.set_password(password)
        user.save()
        return user
    
    def validate(self, data):

        if data.get("password") != data.get("password2"):
            raise serializers.ValidationError({"password" : "Password fields are not matching"})

        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name")
    
class CustomTokenSerializer(TokenSerializer):
    user = UserSerializer(read_only = True)
    class Meta(TokenSerializer.Meta):
        fields = ("key", "user")