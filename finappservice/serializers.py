from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from .models import *
from finappservice.models import *


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = '__all__'


class RoleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class OfficeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = "__all__"