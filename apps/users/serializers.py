from django.contrib.auth import get_user_model
from django_countries.serializer_fields import CountryField
from djoser.serializers import UserCreateSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    # because profile is one to one field with user, that is why we have access to profile fields
    gender = serializers.CharField(source="profile.gender")  
    phone_number = PhoneNumberField(source="profile.phone_number")
    profile_photo = serializers.ImageField(source="profile.profile_photo")
    country = CountryField(source="profile.country")
    city = serializers.CharField(source="profile.city")
    top_seller = serializers.BooleanField(source="profile.top_seller")
    
    #because first name and last name is in user profile
    first_name = serializers.SerializerMethodField() # remember to declare these ttwo metdots
    last_name = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField(source="get_full_name") # this is from user model get_full_name

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "gender",
            "phone_number",
            "profile_photo",
            "country",
            "city",
            "top_seller",
        ]

    def get_first_name(self, obj):
        return obj.first_name.title()

    def get_last_name(self, obj):
        return obj.last_name.title()

    # this below: if user is superuser, than we add to fields "admin"
    def to_representation(self, instance):
        representation = super(UserSerializer, self).to_representation(instance)
        if instance.is_superuser:
            representation["admin"] = True
        return representation

class CreateUserSerializer(UserCreateSerializer): # so we dont need to copy these all fields
    class Meta(UserCreateSerializer.Meta): 
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "password"]            