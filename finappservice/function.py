from finappservice.models import *



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
    