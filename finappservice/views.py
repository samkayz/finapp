from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
from .serializers import *
from datetime import datetime
import random
import string
import uuid
from .models import *


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def role(request):
    name = request.data.get('name')
    desc = request.data.get('description')

    data = {
        "name": name,
        "description": desc
    }
    serializer = RoleCreateSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def roles(request):
    try:
        show = Role.objects.filter()
    except Role.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer = RoleCreateSerializer(instance=show, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createOffice(request):
    name =request.data.get('name')
    openingDate = request.data.get('openingDate')
    parentid = request.data.get('parentid')

    data = {
        "name": name,
        "opening_date": openingDate,
        "parentid": parentid
    }
    serializer = OfficeCreateSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)