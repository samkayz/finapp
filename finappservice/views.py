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
from .function import customerId


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def offices(request):
    try:
        show = Office.objects.filter()
    except Office.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer = OfficeCreateSerializer(instance=show, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createCustomer(request):
    newId = customerId()
    base_date_time = datetime.now()
    submittedDate = (datetime.strftime(base_date_time, "%Y-%m-%d"))
    #Customer Detail
    officeId = request.data.get('officeId')
    firstname = request.data.get('firstname')
    lastname = request.data.get('lastname')
    mnemonic = request.data.get('mnemonic')
    mobileNo = request.data.get('mobileNo')
    active = request.data.get('active')

    # Customer Address
    addressLine = request.data.get('addressLine')
    street = request.data.get('street')
    landmark = request.data.get('landmark')
    country = request.data.get('country')
    state = request.data.get('state')
    district = request.data.get('district')

    # Customer Identification
    modeOfId = request.data.get('modeOfId')
    idNo = request.data.get('idNo')
    if Customer.objects.filter(mnemonic=mnemonic).exists():
        error = {
            "message": "Sorry Mnemonic alrealdy used"
        }
        return Response(data=error, status=status.HTTP_207_MULTI_STATUS)
    else:
        CusData = {
            "customerId": newId,
            "officeId": officeId,
            "firstname": firstname,
            "lastname": lastname,
            "mnemonic": mnemonic,
            "submittedDate": submittedDate,
            "active": active
        }
        cusSerializer = CustomerSerializer(data=CusData)
        if cusSerializer.is_valid():
            cusSerializer.save()

        uid = Customer.objects.values('id').get(mnemonic=mnemonic)['id']

        cusAddress = {
            "userId": uid,
            "addressLine": addressLine,
            "street": street,
            "landmark": landmark,
            "country": country,
            "state": state,
            "mobileNo": mobileNo,
            "district": district,
            "mnemonic": mnemonic
        }
        addSerializer = AddresstableSerializer(data=cusAddress)
        if addSerializer.is_valid():
            addSerializer.save()
    

        Id = {
            "userId": uid,
            "modeOfId": modeOfId,
            "idNo": idNo,
            "mnemonic": mnemonic
        }
        IdSerializer = IdentificationIdSerializer(data=Id)
        if IdSerializer.is_valid():
            IdSerializer.save()

        return Response(data=cusSerializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def allCustomer(request):
   show = Customer.objects.filter()
   serializer = CustomerSerializer(instance=show, many=True)
   return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def customerById(request, customerId):
    mnemonic = Customer.objects.values('mnemonic').get(customerId=customerId)['mnemonic']
    cus = Customer.objects.all().get(mnemonic=mnemonic)
    ad = Addresstable.objects.all().get(mnemonic=mnemonic)
    mn = IdentificationId.objects.all().get(mnemonic=mnemonic)

    data = {
        "profile": {
            "id": cus.id,
            "customerId": cus.customerId,
            "officeId": cus.officeId,
            "firstname": cus.firstname,
            "lastname": cus.lastname,
            "mnemonic": cus.mnemonic,
            "activationDate": cus.activationDate,
            "submittedDate": cus.submittedDate,
            "active": cus.active,
            "address": {
                "data": {
                    "addressLine": ad.addressLine,
                    "street": ad.street,
                    "landmark": ad.landmark,
                    "country": ad.country,
                    "state": ad.state, 
                    "district": ad.district,
                    "mobileNo": ad.mobileNo
                }
            },
            "modeOfId": mn.modeOfId,
            "idNo": mn.idNo
        }
    }
    return Response(data=data, status=status.HTTP_200_OK)
