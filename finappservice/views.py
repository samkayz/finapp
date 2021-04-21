from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet
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
functionClass = App()
from datetime import datetime, timedelta

base_date_time = datetime.now()
now = (datetime.strftime(base_date_time, "%Y-%m-%d"))


@api_view(['POST'])
@permission_classes([])
def createUser(request):
    U = 6
    res = ''.join(random.choices(string.digits, k=U))
    cs = str(res)
    staffid = "STID" + cs
    username = request.data.get('username')
    staffname = request.data.get('staffname')
    email = request.data.get('email')
    role = request.data.get('role')
    password = request.data.get('password')
    re_password = request.data.get('re_password')

    if password == re_password:
        if functionClass.CheckUsername(username) == True:
            data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': "Username Taken"
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
        elif functionClass.CheckEmail(email) == True:
            data = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': "Email Taken"
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            if role == 'tl' or role == 'cs':
                functionClass.RegisterUser(username, staffname, email, role, password, staffid)
                data = {
                    'status': status.HTTP_200_OK,
                    "staffID": staffid,
                    "message": "registration successful"
                }
                return Response(data=data, status=status.HTTP_200_OK)
                
            else:
                data = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': "Invalid Role"
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        data = {
            'status': status.HTTP_400_BAD_REQUEST,
            'message': "password mismatch"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def allUser(request):
    try:
        userSnippet = User.objects.all()
    except: User.DoesNotExist

    if functionClass.CheckIfSuperLoginUser(request) == False:
        data = {
            "code": status.HTTP_200_OK,
            "message": "Permission Denied"
        }
        return Response(data=data, status=status.HTTP_200_OK)
    
    else:
        user = userSerializer(instance=userSnippet, many=True)
        return Response(data=user.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteUser(request, id):
    try:
        userDetails = get_object_or_404(User, id=id)
        if functionClass.CheckIfSuperLoginUser(request) == False:
            data = {
                "code": status.HTTP_200_OK,
                "message": "Permission Denied"
            }
            return Response(data=data, status=status.HTTP_200_OK)
        elif userDetails.is_superuser == True:
            data = {
                "code": status.HTTP_200_OK,
                "message": "You can't delete this user"
            }
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            ## Delete User Instance
            delUser = User.objects.filter(id=id)
            delUser.delete()

            ## Delete Customer Service Instance
            dltCust = CustomerService.objects.filter(user_id=id)
            dltCust.delete()

            ## Delete Teller Instance
            dltTell = Teller.objects.filter(user_id=id)
            dltTell.delete()


            data = {
                "code": status.HTTP_200_OK,
                "message": "User deleted"
            }
            return Response(data=data, status=status.HTTP_200_OK)
    except:
        data = {
            'status': status.HTTP_400_BAD_REQUEST,
            'message': "Permission Denied"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createOffice(request):
    U = 4
    res = ''.join(random.choices(string.digits, k=U))
    cs = str(res)
    branchcode = "B" + cs
    name =request.data.get('name')
    
    if functionClass.CheckIfSuperLoginUser(request) == False:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Permissinon Denied"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    else:
        if Branch.objects.filter(name=name).exists():
            data = {
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Office Name Exist.....",
                "status": "fail"
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = {
                "code": status.HTTP_201_CREATED,
                "name": name,
                "branchcode": branchcode
            }
            serializer = BranchCreateSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def offices(request):
    if functionClass.CheckIfSuperLoginUser(request) == False:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Permissinon Denied"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            show = Branch.objects.filter()
        except Branch.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = BranchCreateSerializer(instance=show, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createCustomer(request):
    newId = functionClass.customerId()
    submittedDate = (datetime.strftime(base_date_time, "%Y-%m-%d"))
    #Customer Detail
    branch = request.data.get('branchid')
    firstname = request.data.get('firstname')
    lastname = request.data.get('lastname')
    mnemonic = request.data.get('mnemonic')
    mobileNo = request.data.get('mobileNo')

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
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Sorry Mnemonic alrealdy used",
            "status": "fail"
        }
        return Response(data=error, status=status.HTTP_207_MULTI_STATUS)
    else:
        functionClass.CreateCustomer(branch, newId, firstname, lastname, mnemonic, addressLine, street, landmark, country, state, district, mobileNo, modeOfId, idNo)
        data = {
            "code": status.HTTP_200_OK,
            "status": "success",
            "CustomerID": newId,
            "submittedDate": submittedDate
        }

        return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def allCustomer(request):
   show = Customer.objects.filter()
   serializer = CustomerSerializer(instance=show, many=True)
   return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def customerById(request, customerId):
    show = Customer.objects.filter(customerId=customerId)
    serializer = CustomerSerializer(instance=show, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def acctCategory(request):
    name = request.data.get('name')

    if AccountType.objects.filter(name=name).exists():
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Account Name exist",
            "status": "fail"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    else:
        data = {
            "name": name
        }
        serializer = AccountCategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def allAcctCategory(request):
    try:
        show = AccountType.objects.filter()
    except AccountType.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    serializer = AccountCategorySerializer(instance=show, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def openAccount(request):
    customerId = request.data.get('customerId')
    accountTypeId = request.data.get('accountTypeId')

    try:
        cust = Customer.objects.all().get(customerId=customerId)
        actype = AccountType.objects.all().get(id=accountTypeId)

        if Account.objects.filter(customerId=customerId, accountTypeId=accountTypeId).exists():
            data = {
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Customer have same type of account",
                "status": "fail"
            }
            return Response(data=data)
        else:
            newAccount = functionClass.AccountNumber()
            data = {
                "customer": cust.id,
                "customerId": customerId,
                "mnemonic": cust.mnemonic,
                "accounNumber": newAccount,
                "accountTypeId": actype.id,
                "accountType": actype.name,
                "createdBy": request.user.staffname,
                "accountName": cust.firstname + ' ' + cust.lastname,
            }
            serializer = AccountSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
    except:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "customer ID/Account type not exist",
            "status": "fail"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def customerAccount(request, customerId):

    try:
        show = Customer.objects.filter(customerId=customerId)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer = ViewCustomerAccountsSerializer(instance=show, many=True)
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
    tellerId = functionClass.TellerId()
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
        tba = TellerBalance.objects.filter(tellerId=tellerId, openDate=openOn).exists()
    except:
        error = {
            "message": "TellerId not Found"
        }
        return Response(data=error, status=status.HTTP_207_MULTI_STATUS)
    if tba:
        msg = {
            "message": "Teller Business Already Open for the day"
        }
        return Response(data=msg, status=status.HTTP_200_OK)
    else:
        data = {
            "user": tid.user_id,
            "tellerId": tid.tellerId,
            "openDate": openOn,
            "openBal": openBal,
            "bal": openBal
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
    client = twilioAuth()
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
    phone = Addresstable.objects.values('mobileNo').get(mnemonic=c_acct.mnemonic)['mobileNo']
    #Teller Detail
    tdetail = Teller.objects.all().get(tellerId=tellerId)
    t_bal = TellerBalance.objects.all().get(tellerId=tellerId, openDate=tday)

    rp = list(acctNo)
    rp[5] = '*'
    rp[6] = '*'
    rp[7] = '*'
    rp[8] = '*'
    ac_rp = ''.join([str(elem) for elem in rp])
    #print(ac_rp)
    if t_bal.status == 'close':
        err = {
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "Teller operation is closed for the day"
        }
        return Response(data=err, status=status.HTTP_400_BAD_REQUEST)
    elif transType == "CR":
        # Get Customer Balance

        #Update Previous Balance
        pbal = c_acct.workingBalance
        Account.objects.filter(accounNumber=acctNo).update(previousBalance=pbal)

        # Update Working Balance 
        wbal = c_acct.workingBalance + amt
        Account.objects.filter(accounNumber=acctNo).update(workingBalance=wbal)

        #Update Teller Balance
        tbal = t_bal.bal + amt
        TellerBalance.objects.filter(tellerId=tellerId, openDate=tday).update(bal=tbal)

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

        #Send Message to Customer

        # message = client.messages.create(
        # to=phone, 
        # from_="+12018906990",
        # body=f'Acct: {ac_rp} \n Ref: {tranId}\n TranType: CR \n Amount: {amt}\n Date: {tday}\n From: {senderName}\n ThankYou for Banking with Us')

        #print(message.sid)
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
            TellerBalance.objects.filter(tellerId=tellerId, openDate=tday).update(bal=tbal)

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
        # message = client.messages.create(
        # to=phone, 
        # from_="+12018906990",
        # body=f'Acct: {ac_rp} \n Ref: {tranId}\n TranType: DR \n Amount: {amt}\n Date: {tday}\n From: {senderName}\n ThankYou for Banking with Us')

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



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def closeBal(request):
    tellerId = request.data.get('tellerId')
    user_id = request.user.id
    base_date_time = datetime.now()
    tday = (datetime.strftime(base_date_time, "%Y-%m-%d"))

    try:
        cbal = get_object_or_404(TellerBalance, tellerId=tellerId, openDate=tday)
        # cbal = TellerBalance.objects.all().get(tellerId=tellerId, openDate=tday)
    except:
        error = {
            "message": "Permission denied"
        }
        return Response(data=error, status=status.HTTP_204_NO_CONTENT)
    
    if cbal.status == "open":
        # Update Close Balance
        TellerBalance.objects.filter(user_id=user_id, openDate=tday).update(closeBal=cbal.bal)

        # Update Close Date
        TellerBalance.objects.filter(user_id=user_id, openDate=tday).update(closeDate=tday)

        #Total Transaction 
        t_trans = cbal.bal - cbal.openBal

        TellerBalance.objects.filter(user_id=user_id, openDate=tday).update(totaltran=t_trans)

        # Close the Status
        TellerBalance.objects.filter(user_id=user_id, openDate=tday).update(status='close')

        sus = {
            "message": "Teller Close for the day business"
        }
        return Response(data=sus, status=status.HTTP_200_OK)
    else:
        msg = {
            "message": "Teller Business already close for the day"
        }
        return Response(data=msg, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_loan(request):
    U = 4
    res1 = ''.join(random.choices(string.digits, k=U))
    loan_code = str(res1)
    loanName = request.data.get('loanName')
    loan_duration = request.data.get('duration')

    if request.user.is_superuser == False:
        data = {
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "Permission denied"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    elif LoanType.objects.filter(Q(loan_name__startswith=loanName) | Q(loan_name__endswith=loanName)):
        data = {
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "Name already exist"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        createLoanType = LoanType(loan_name=loanName, loan_code=loan_code, loan_duration=loan_duration)
        prod = Products(product_code=loan_code, product_name=loanName)
        createLoanType.save()
        prod.save()
        data = {
            "code": status.HTTP_200_OK,
            "success": True, 
            "response": {
                "loanCode": loan_code,
                "loanName": loanName
            }
        }
        return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def loanApply(request):
    base_date_time = datetime.now()
    tday = (datetime.strftime(base_date_time, "%Y-%m-%d"))
    U = 6
    res1 = ''.join(random.choices(string.digits, k=U))
    lid = str(res1)
    accountNumber = request.data.get('accountNumber')
    loanAmount = request.data.get('loanAmount')
    loanOfficer = request.data.get('loanOfficer')
    loanType = request.data.get('loanCode')

    if Account.objects.filter(accounNumber=accountNumber).exists() == False:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "success": False, 
            "response": {
                "loanCode": "Invalid Account/ Account doesn't exist"
            }
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    elif LoanType.objects.filter(loan_code=loanType).exists() == False:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "success": False, 
            "response": {
                "loanCode": "Invalid Loan ID/ Loan Type doesn't exist"
            }
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    elif LoanApplication.objects.filter(accountNumber=accountNumber, loan_paid=False).exists():
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "success": False, 
            "response": {
                "message": "This customer have unpaid Loan"
            }
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    else:
        cusId = get_object_or_404(Account, accounNumber=accountNumber)
        custDetail = get_object_or_404(Customer, customerId=cusId.customerId)
        loanDetail = get_object_or_404(LoanType, loan_code=loanType)
    
        createLoan = LoanApplication(loanId=lid, 
        customerId=cusId.customerId, 
        accountNumber=cusId.accounNumber, 
        customerName=cusId.accountName, 
        loanAmount=loanAmount, 
        dateApply=tday, 
        loanOfficer=loanOfficer, duration=loanDetail.loan_duration,
        loan_code=loanType, loanBal=loanAmount, customer_id=custDetail.id)
        createLoan.save()
        # serializer = LoanApplicationSerializer(data=data)
        # if serializer.is_valid():
        #     serializer.save()
        stat = {
            "status": {
                "status": status.HTTP_200_OK,
                "loanId": lid
                },
            "message": "Loan Application successful and waiting for approval"
        }
        return Response(data=stat, status=status.HTTP_200_OK)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def allLoan(request):
    try:
        show = LoanApplication.objects.filter()
    except LoanApplication.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    serializer = LoanApplicationSerializer(instance=show, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approveLoan(request):
    base_date_time = datetime.now()
    tday = (datetime.strftime(base_date_time, "%Y-%m-%d"))
    loanId = request.data.get('loanId')
    try:
        loan = get_object_or_404(LoanApplication, loanId=loanId)
    except:
        error = {
            "status": {
                "status": status.HTTP_204_NO_CONTENT
            },
            "message": "Wrong Loan ID/Loan not Exist"
        }
        return Response(data=error, status=status.HTTP_204_NO_CONTENT)
    
    if loan.loan_approve == True:
        dt = datetime.now()
        td = loan.pay_day
        print(td)
        print(dt)
        msg = {
            "message": f'Loan with ID {loanId} Already Approved'
        }
        return Response(data=msg, status=status.HTTP_208_ALREADY_REPORTED)
    else:
        acct = get_object_or_404(Account, accounNumber=loan.accountNumber)
        no_of_days = loan.duration
        dt = datetime.now()
        td = timedelta(days=no_of_days)
        pay_date = dt + td
        # Update loan status
        LoanApplication.objects.filter(loanId=loan.loanId).update(loan_approve=True, dateApprove=tday, pay_day=pay_date)

        ## Add the Loan Amount to the customer account Number
        bal = acct.workingBalance
        loan_amount = loan.loanAmount
        newBal = bal + loan_amount

        update_account = Account.objects.filter(accounNumber=acct.accounNumber)
        update_account.update(previousBalance=bal, workingBalance=newBal)

        ## Create Transaction Log
        senderName = 'Loan'
        comment = 'Loan Disbursement'
        functionClass.createLog(loan.loanAmount, senderName, senderName, loan.customerName, loan.accountNumber, comment)
        data = {
            "code": status.HTTP_200_OK,
            "success": True, 
            "response": {
                "message": f'{loan.loanAmount} has been approved for {loan.customerName}'
            }
        }
        return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def smsTwilio(request):
    accountSid = request.data.get('twilioAccountId')
    token = request.data.get('token')

    if accountSid == "" or token == "":
        err = {
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "Twilio Account ID/ Token Can't be empty"
        }
        return Response(data=err, status=status.HTTP_400_BAD_REQUEST)
    elif Twilio.objects.filter(smsName='twilio').exists():
        Twilio.objects.filter(smsName='twilio').update(account_sid=accountSid, auth_token=token)
        sucess = {
            "status": status.HTTP_200_OK,
            "message": "twilio account updated"
        }
        return Response(data=sucess, status=status.HTTP_200_OK)
    else:
        data = {
            "account_sid": accountSid,
            "auth_token": token
        }
        tsms = TwilioSerializer(data=data)
        if tsms.is_valid():
            tsms.save()
        return Response(data=tsms.data, status=status.HTTP_200_OK)
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_internal_account(request):
    productCode = request.data.get('productCode')
    accountName = request.data.get('accountName')
    
    if request.user.is_superuser == False:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Bad Request/Permission Denied"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    elif productCode == '':
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "product code can't be empty"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    elif functionClass.checkProduct(productCode) == False:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Invalid product code"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    elif accountName == '':
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Account Name can't be empty"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    elif InternalAccount.objects.filter(product_code=productCode).exists():
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Internal Account for this product exist"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        acctNo = functionClass.InternalAccountNumber()
        functionClass.createInternalAccount(productCode, accountName, acctNo)
        
        data = {
            "code": status.HTTP_200_OK,
            "success": True,
            "message": "created"
        }
        return Response(data=data, status=status.HTTP_200_OK)
    
    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteInternaAccount(request, code):
    if request.user.is_superuser == False:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Bad Request/Permission Denied"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    elif InternalAccount.objects.filter(product_code=code).exists() == False:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Bad Request/Wrong Product Code"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        deleteInstance = InternalAccount.objects.filter(product_code=code)
        deleteInstance.delete()
        data = {
            "code": status.HTTP_200_OK,
            "success": True,
            "message": "internal account deleted"
        }
        return Response(data=data, status=status.HTTP_200_OK)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateInternalAccount(request, code):
    accountName = request.data.get('accountName')
    if request.user.is_superuser == False:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Bad Request/Permission Denied"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    elif InternalAccount.objects.filter(product_code=code).exists() == False:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Invalid product code"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    elif accountName == '':
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Account name can't be empty"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        updateInstance = InternalAccount.objects.filter(product_code=code)
        updateInstance.update(product_name=accountName)
        data = {
            "code": status.HTTP_200_OK,
            "success": True,
            "message": "internal account updated"
        }
        return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def allInternalAccount(request):
    if request.user.is_superuser == False:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Bad Request/Permission Denied"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        snippet = InternalAccount.objects.filter()
        serializer = InternalAccountSerializer(instance=snippet, many=True)
        data = {
            "code": status.HTTP_200_OK,
            "success": True,
            "content": serializer.data
        }
        return Response(data=data, status=status.HTTP_200_OK)
    
   
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addCurrency(request):
    currencyCode = request.data.get('currencyCode')
    currencyName = request.data.get('currencyName')
    active = request.data.get('active')
    
    if currencyCode is None:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "currencyCode Fields required"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    elif currencyName is None:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "currencyName Fields required"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    elif request.user.is_superuser == False:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Bad Request/Permission Denied"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    elif currencyCode == "":
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Currency Code can't be empty"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    elif currencyName == "":
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Currency Name can't be empty"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    elif active == "" or type(active) != bool:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Currency active must be boolean True/False"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    elif Currency.objects.filter(cur_code=currencyCode).exists():
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Currency Exist"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        if active == True:
            Currency.objects.filter(active=True).update(active=False)
            
            crt_cur = Currency(cur_code=currencyCode, cur_name=currencyName, active=True)
            crt_cur.save()
            data = {
                "code": status.HTTP_200_OK,
                "success": True,
                "message": "Currency Created"
            }
            return Response(data=data, status=status.HTTP_200_OK)
            
        else:
            crt_cur = Currency(cur_code=currencyCode, cur_name=currencyName)
            crt_cur.save()
            data = {
                "code": status.HTTP_200_OK,
                "success": True,
                "message": "Currency Created"
            }
            return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def allCurrency(request):
    if request.user.is_superuser == False:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Bad Request/Permission Denied"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    else:
        snippet = Currency.objects.filter()
        serializedData = CurrencySerializer(instance=snippet, many=True)
        data = {
            "code": status.HTTP_200_OK,
            "success": True,
            "content": serializedData.data
        }
        return Response(data=data, status=status.HTTP_200_OK)
    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteCurrency(request, code):
    if request.user.is_superuser == False:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Bad Request/Permission Denied"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    elif Currency.objects.filter(cur_code=code).exists() == False:
        data = {
            "code": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Invalid Currency Code"
        }
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        Currency.objects.filter(cur_code=code).delete()
        data = {
            "code": status.HTTP_200_OK,
            "success": True,
            "message":" Currency deleted"
        }
        return Response(data=data, status=status.HTTP_200_OK)