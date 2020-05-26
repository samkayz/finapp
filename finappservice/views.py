from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
UserModel = get_user_model()
from django.db.models import Q
from .serializers import *
from datetime import datetime
import random
import string
import uuid
from .models import *
from .function import *


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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def acctCategory(request):
    name = request.data.get('name')
    accountId = request.data.get('accountId')

    data = {
        "name": name,
        "accountId": accountId
    }
    serializer = AccountCategorySerializer(data=data)
    if serializer.is_valid():
        serializer.save()
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def allAcctCategory(request):
    try:
        show = AccountCategory.objects.filter()
    except AccountCategory.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    serializer = AccountCategorySerializer(instance=show, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def openAccount(request):
    base_date_time = datetime.now()
    openOn = (datetime.strftime(base_date_time, "%Y-%m-%d"))
    customerId = request.data.get('customerId')
    accountTypeId = request.data.get('accountTypeId')
    active = request.data.get('active')

    try:
        cust = Customer.objects.all().get(customerId=customerId)
        actype = AccountCategory.objects.all().get(accountId=accountTypeId)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if accountTypeId == 1:
        newAccount = AccountNumber()
        data = {
            "customerId": customerId,
            "mnemonic": cust.mnemonic,
            "accountName": cust.firstname + ' ' + cust.lastname,
            "accounNumber": newAccount,
            "ledgerBalance": 0,
            "workingBalance": 0,
            "accountTypeId": actype.accountId,
            "accountType": actype.name,
            "active": active,
            "createdBy": request.user.first_name + ' ' + request.user.last_name,
            "openOn": openOn
        }
        serializer = AccountSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif accountTypeId == 2:
        newAccount = AccountNumber()
        data = {
            "customerId": customerId,
            "mnemonic": cust.mnemonic,
            "accountName": cust.firstname + ' ' + cust.lastname,
            "accounNumber": newAccount,
            "ledgerBalance": 0,
            "workingBalance": 0,
            "accountTypeId": actype.accountId,
            "accountType": actype.name,
            "active": active,
            "createdBy": request.user.first_name + ' ' + request.user.last_name,
            "openOn": openOn
        }
        serializer = AccountSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    else:
        newAccount = AccountNumber()
        data = {
            "customerId": customerId,
            "mnemonic": cust.mnemonic,
            "accountName": cust.firstname + ' ' + cust.lastname,
            "accounNumber": newAccount,
            "ledgerBalance": 0,
            "workingBalance": 0,
            "accountTypeId": actype.accountId,
            "accountType": actype.name,
            "active": active,
            "createdBy": request.user.first_name + ' ' + request.user.last_name,
            "openOn": openOn
        }
        serializer = AccountSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def customerAccount(request, customerId):

    try:
        show = Account.objects.filter(customerId=customerId)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer = AccountSerializer(instance=show, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def fundTransfer(request):
    base_date_time = datetime.now()
    openOn = (datetime.strftime(base_date_time, "%Y-%m-%d"))
    debitAccount = request.data.get('debitAccount')
    creditAccount = request.data.get('creditAccount')
    amount = request.data.get('amount')
    comment = request.data.get('comment')
    newId = ftId()

    checkAccount = Account.objects.values('workingBalance').get(accounNumber=debitAccount)['workingBalance']
    if checkAccount < float(amount):
        error = {
            "message": "Insufficient Account Balance"
        }
        return Response(data=error, status=status.HTTP_207_MULTI_STATUS)
    else:
        # credit Account Information
        crdAcct = Account.objects.all().get(accounNumber=creditAccount)

        # Debit Account Details
        dbtAcct = Account.objects.all().get(accounNumber=debitAccount)

        # Update sender previous balance
        Account.objects.filter(accounNumber=debitAccount).update(previousBalance=checkAccount)

        # Update receiver's previous Balance
        Account.objects.filter(accounNumber=creditAccount).update(previousBalance=crdAcct.workingBalance)

        # Debit Sender
        NewAmount = float(amount)
        New = dbtAcct.workingBalance - NewAmount

        Account.objects.filter(accounNumber=debitAccount).update(workingBalance=New)


        # Credit Receiver
        New2 = crdAcct.workingBalance + NewAmount
        Account.objects.filter(accounNumber=creditAccount).update(workingBalance=New2)

        tdata = {
            "transId": newId,
            "transDate": openOn,
            "transAmount": amount,
            "senderName": dbtAcct.accountName,
            "senderAccount": dbtAcct.accounNumber,
            "receiverName": crdAcct.accountName,
            "receiverAccount": crdAcct.accounNumber,
            "comment": comment
        }

        serializer = TransactionSerializer(data=tdata)
        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def allTrasaction(request):
    try:
        show = TransactionHistory.objects.filter()
    except TransactionHistory.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer = TransactionSerializer(instance=show, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transById(request, transId):
    try:
        show = TransactionHistory.objects.filter(transId=transId)
    except TransactionHistory.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer = TransactionSerializer(instance=show, many=True)

    return Response(data=serializer.data, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assignTeller(request):
    tellerId = TellerId()
    user_id = request.data.get('userId')

    try:
        all_ = UserModel.objects.all().get(id=user_id)
    except:
        error = {
            "message": "UserID is not a registered User"
        }
        return Response(data=error, status=status.HTTP_207_MULTI_STATUS)

    if Teller.objects.filter(user_id=user_id).exists():
        error = {
            "message": "User already added to Teller"
        }
        return Response(data=error, status=status.HTTP_207_MULTI_STATUS)
    else:
        data = {
            "user_id": user_id,
            "tellerId": tellerId,
            "tellerName": all_.first_name + ' ' + all_.last_name
        }
        serializer = TellerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def openBal(request):
    base_date_time = datetime.now()
    openOn = (datetime.strftime(base_date_time, "%Y-%m-%d"))
    tellerId = request.data.get('tellerId')
    openBal = request.data.get('openBal')

    try:
        tid = Teller.objects.all().get(tellerId=tellerId)
    except expression as identifier:
        error = {
            "message": "TellerId not Found"
        }
        return Response(data=error, status=status.HTTP_207_MULTI_STATUS)

    data = {
        "user_id": tid.user_id,
        "tellerId": tid.tellerId,
        "openDate": openOn,
        "openBal": openBal
    }
    serializer = TellerBalanceSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def checkCurrentTellerBal(request, telleId):
    base_date_time = datetime.now()
    today = (datetime.strftime(base_date_time, "%Y-%m-%d"))

    try:
        show = TellerBalance.objects.filter(tellerId=telleId, openDate=today)
    except:
        error = {
            "message": "Wrong TellerId"
        }
        return Response(data=error, status=status.HTTP_207_MULTI_STATUS)
    serializer = TellerBalanceSerializer(instance=show, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def operate(request):
    U = 10
    res1 = ''.join(random.choices(string.digits, k=U))
    txn1 = str(res1)
    tranId = "TR|" + txn1
    base_date_time = datetime.now()
    tday = (datetime.strftime(base_date_time, "%Y-%m-%d"))
    acctNo = request.data.get('accountNumber')
    transType = request.data.get('transType')
    amount = request.data.get('amount')
    tellerId = request.data.get('tellerId')
    senderName = request.data.get('senderName')
    receiverName = request.data.get('receiverName')
    comment = request.data.get('comment')

    amt = float(amount)
    c_acct = Account.objects.all().get(accounNumber=acctNo)
    #Teller Detail
    tdetail = Teller.objects.all().get(tellerId=tellerId)
    t_bal = TellerBalance.objects.all().get(tellerId=tellerId)

    if transType == "CR":
        # Get Customer Balance

        #Update Previous Balance
        pbal = c_acct.workingBalance
        Account.objects.filter(accounNumber=acctNo).update(previousBalance=pbal)

        # Update Working Balance 
        wbal = c_acct.workingBalance + amt
        Account.objects.filter(accounNumber=acctNo).update(workingBalance=wbal)

        #Update Teller Balance
        tbal = t_bal.bal + amt
        TellerBalance.objects.filter(tellerId=tellerId).update(bal=tbal)

        #Update Teller Transaction History

        tdata = {
            "user_id": t_bal.user_id,
            "tellerId": t_bal.tellerId,
            "transAmount": amt,
            "transAccount": acctNo,
            "transType": "CR",
            "transDate": tday,
            "tellerName": tdetail.tellerName
        }
        tdataserializer = TellerTransactionHistorySerializer(data=tdata)
        if tdataserializer.is_valid():
            tdataserializer.save()

        #Update Customer History
        cdata = {
            "transId": tranId,
            "transDate": tday,
            "transAmount": amt,
            "senderName": senderName,
            "receiverName": c_acct.accountName,
            "receiverAccount": acctNo,
            "comment": comment
        }
        cdataserializer = TransactionSerializer(data=cdata)
        if cdataserializer.is_valid():
            cdataserializer.save()
    else:
        if amt > c_acct.workingBalance:
            error = {
                "message": "Insufficient Balance"
            }
            return Response(data=error, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # Get Customer Balance

            #Update Previous Balance
            pbal = c_acct.workingBalance
            Account.objects.filter(accounNumber=acctNo).update(previousBalance=pbal)

            # Update Working Balance 
            wbal = c_acct.workingBalance - amt
            Account.objects.filter(accounNumber=acctNo).update(workingBalance=wbal)

            #Update Teller Balance
            tbal = t_bal.bal - amt
            TellerBalance.objects.filter(tellerId=tellerId).update(bal=tbal)

            #Update Teller Transaction History

            tdata = {
                "user_id": t_bal.user_id,
                "tellerId": t_bal.tellerId,
                "transAmount": amt,
                "transAccount": acctNo,
                "transType": "DR",
                "transDate": tday,
                "tellerName": tdetail.tellerName
            }
            tdataserializer = TellerTransactionHistorySerializer(data=tdata)
            if tdataserializer.is_valid():
                tdataserializer.save()

            #Update Customer History
            cdata = {
                "transId": tranId,
                "transDate": tday,
                "transAmount": amt,
                "senderName": senderName,
                "receiverName": c_acct.accountName,
                "receiverAccount": acctNo,
                "comment": comment
            }
            cdataserializer = TransactionSerializer(data=cdata)
            if cdataserializer.is_valid():
                cdataserializer.save()

    suc = {
        "message": "Transaction Successful"
    }
    return Response(data=suc, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enquiry(request):
    acctNo = request.data.get('accountNumber')
    transDate = request.data.get('transDate')
    transId = request.data.get('transId')

    try:
        show = TransactionHistory.objects.filter(Q(receiverAccount=acctNo) | Q(transDate=transDate) | Q(transId=transId))
    except:
        error = {
            "message": "Invalid parameter or Detail not Found"
        }
        return Response(data=error, status=status.HTTP_401_UNAUTHORIZED)
    
    serializer = TransactionSerializer(instance=show, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


