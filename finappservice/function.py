from finappservice.models import *
from twilio.rest import Client
import random
import string
from django.shortcuts import get_object_or_404



class App:

    def customerId(self):
        last_id = Customer.objects.all().order_by('id').last()
        if not last_id:
            return '100000'
        customerId = last_id.customerId
        id_int = int(customerId)
        new_idNo = id_int + 1
        return new_idNo


    def AccountNumber(self):
        last_act = Account.objects.all().order_by('id').last()
        if not last_act:
            return '1000000000'
        AccountNumberId = last_act.accounNumber
        acct_int = int(AccountNumberId)
        newAccountNumber = acct_int + 1
        return newAccountNumber
    
    def InternalAccountNumber(self):
        last_act = InternalAccount.objects.all().order_by('id').last()
        if not last_act:
            return '7000000000'
        AccountNumberId = last_act.accounNumber
        acct_int = int(AccountNumberId)
        newAccountNumber = acct_int + 1
        return newAccountNumber


    def ftId(self):
        lastId = TransactionHistory.objects.all().order_by('id').last()
        if not lastId:
            return 'FT10000000'
        fundTransferId = lastId.transId
        tId = int(fundTransferId.split('FT')[-1])
        print(tId)
        newTransId = tId + 1
        newTrans = 'FT' + str(newTransId)
        return newTrans


    def TellerId(self):
        last_id = Teller.objects.all().order_by('id').last()
        if not last_id:
            return '1000'
        tellerIdNo = last_id.tellerId
        tellerIdNo_int = int(tellerIdNo)
        newId = tellerIdNo_int + 1
        return newId


    def twilioAuth(self):
        twilio = Twilio.objects.all().get(smsName='twilio')
        account_sid = twilio.account_sid
        auth_token  = twilio.auth_token
        client = Client(account_sid, auth_token)
        return client


    # def accountType(self):
    #     last_id = AccountCategory.objects.all().order_by('id').last()
    #     if not last_id:
    #         return '1'
    #     acctId = int(last_id.accountId)
    #     newId = acctId + 1
    #     return newId


    def RegisterUser(self, username, staffname, email, role, password, staffid):
        if role == "tl":
            user = User.objects.create_user(username=username, staffname=staffname, email=email, staffid=staffid, is_teller=True, password=password)
            user.save()
            teller = Teller(tellerId=staffid, tellerName=staffname, user=user)
            teller.save()
            pass
        else:
            user = User.objects.create_user(username=username, staffname=staffname, staffid=staffid, email=email, is_customer_service=True, password=password)
            user.save()
            cs = CustomerService(staffid=staffid, staffname=staffname, user=user)
            cs.save()
            pass


    def CheckUsername(self, username):
        if User.objects.filter(username=username).exists():
            return True
        else:
            return False


    def CheckEmail(self, email):
        if User.objects.filter(email=email).exists():
            return True
        else:
            return False

    def CheckOffice(self, parentid):
        if User.objects.filter(officeid=parentid).exists():
            return True
        else:
            return False

    def CheckIfSuperLoginUser(self, request):
        if request.user.is_teller == True or request.user.is_customer_service == True:
            return False
        else:
            return True
    

    def CreateCustomer(self, branchid, customerId, firstname, lastname, mnemonic, addressLine, street, landmark, country, state, district, mobileNo, modeOfId, idNo):
        customer = Customer(branchcode=branchid, customerId=customerId, firstname=firstname, lastname=lastname, mnemonic=mnemonic)
        customer.save()
        CustAdd = Addresstable(customer=customer, addressLine=addressLine, street=street, landmark=landmark, country=country, state=state, district=district, mobileNo=mobileNo, mnemonic=mnemonic)
        CustAdd.save()
        ModeOfId = IdentificationId(customer=customer, modeOfId=modeOfId, idNo=idNo, mnemonic=mnemonic)
        ModeOfId.save()
        pass

    
    def createLog(self, transAmount, senderName, senderAccount, receiverName, receiverAccount, comment):
        U = 16
        res1 = ''.join(random.choices(string.digits, k=U))
        txnId = str(res1)
        create_log = TransactionHistory(transId=txnId, 
                                        transAmount=transAmount, senderName=senderName, 
                                        senderAccount=senderAccount, receiverName=receiverName,
                                        receiverAccount=receiverAccount, comment=comment)
        create_log.save()
        pass
    
    def checkProduct(self, code):
        if Products.objects.filter(product_code=code).exists() == True:
            return True
        else:
            return False
    
    def createInternalAccount(self, product_code, product_name, account_number):
        create_internal = InternalAccount(product_code=product_code, product_name=product_name, account_number=account_number)
        create_internal.save()
        pass
    
    
    def UpdateInternalAccountBal(self, product_code, amount, frm_acct, comment):
        U = 16
        res1 = ''.join(random.choices(string.digits, k=U))
        txnId = str(res1)
        acct = get_object_or_404(InternalAccount, product_code=product_code)
        product = get_object_or_404(Products, product_code=product_code)
        bal = acct.working_bal
        amt = float(amount)
        newBal = (amt + bal)
        InternalAccount.objects.filter(product_code=product_code).update(prev_bal=bal, working_bal=newBal)
        
        ##  Create Internal Wallet Log
        log = InternalTransactHistory(product_code=product_code, txn_id=txnId, frm_acct=frm_acct, amount=amount, to_acct=acct.account_number, comment=comment, product_name=product.product_name)
        log.save()
        pass

    def calculateLoanInterest(self, amount, loan_code):
        ln_p = get_object_or_404(LoanType, loan_code=loan_code)
        amt = float(amount)
        intrate = float(ln_p.interest)
        interestAmount = amt * intrate / 100
        finalInterest = round(interestAmount, 2)
        return finalInterest