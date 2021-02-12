from finappservice.models import *
from twilio.rest import Client



def customerId():
    last_id = Customer.objects.all().order_by('id').last()
    if not last_id:
        return '100000'
    customerId = last_id.customerId
    id_int = int(customerId)
    new_idNo = id_int + 1
    return new_idNo


def AccountNumber():
    last_act = Account.objects.all().order_by('id').last()
    if not last_act:
        return '1000000000'
    AccountNumberId = last_act.accounNumber
    acct_int = int(AccountNumberId)
    newAccountNumber = acct_int + 1
    return newAccountNumber


def ftId():
    lastId = TransactionHistory.objects.all().order_by('id').last()
    if not lastId:
        return 'FT10000000'
    fundTransferId = lastId.transId
    tId = int(fundTransferId.split('FT')[-1])
    print(tId)
    newTransId = tId + 1
    newTrans = 'FT' + str(newTransId)
    return newTrans


def TellerId():
    last_id = Teller.objects.all().order_by('id').last()
    if not last_id:
        return '1000'
    tellerIdNo = last_id.tellerId
    tellerIdNo_int = int(tellerIdNo)
    newId = tellerIdNo_int + 1
    return newId


def twilioAuth():
    twilio = Twilio.objects.all().get(smsName='twilio')
    account_sid = twilio.account_sid
    auth_token  = twilio.auth_token
    client = Client(account_sid, auth_token)
    return client


def accountType():
    last_id = AccountCategory.objects.all().order_by('id').last()
    if not last_id:
        return '1'
    acctId = int(last_id.accountId)
    newId = acctId + 1
    return newId


def RegisterUser(username, firstname, lastname, email, officeid, roleid, password):
    create = User.objects.create_user(username=username, first_name=firstname, last_name=lastname, email=email, officeid=officeid, roleid=roleid, password=password)
    create.save()


def CheckUsername(username):
    if User.objects.filter(username=username).exists():
        return True
    else:
        return False


def CheckEmail(email):
    if User.objects.filter(email=email).exists():
        return True
    else:
        return False

def CheckOffice(parentid):
    if User.objects.filter(officeid=parentid).exists():
        return True
    else:
        return False