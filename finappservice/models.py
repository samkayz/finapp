from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    officeid = models.IntegerField()
    roleid = models.IntegerField()
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'last_name', 'password', 'officeid', 'roleid']
    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'user'

    def get_username(self):
        return self



class Role(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        db_table = 'role'


class Office(models.Model):
    name = models.CharField(max_length=255)
    opening_date = models.CharField(max_length=255)
    parentid = models.IntegerField()

    class Meta:
        db_table = 'office'


class Customer(models.Model):
    customerId = models.CharField(max_length=255, null=True, blank=True)
    officeId = models.IntegerField()
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    mnemonic = models.CharField(max_length=100)
    activationDate = models.CharField(max_length=255, null=True, blank=True)
    submittedDate = models.CharField(max_length=255)
    active = models.BooleanField()

    class Meta:
        db_table = 'customer'


class Addresstable(models.Model):
    userId = models.IntegerField()
    addressLine = models.TextField()
    street = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    mobileNo = models.CharField(max_length=255)
    mnemonic = models.CharField(max_length=255)

    class Meta:
        db_table = 'addresstable'

class IdentificationId(models.Model):
    userId = models.IntegerField()
    modeOfId = models.CharField(max_length=255)
    idNo = models.CharField(max_length=255)
    mnemonic = models.CharField(max_length=255)

    class Meta:
        db_table = 'identification_id'


class Account(models.Model):
    customerId = models.CharField(max_length=255)
    mnemonic = models.CharField(max_length=255)
    accountName = models.TextField()
    accounNumber = models.CharField(max_length=255)
    previousBalance = models.FloatField()
    workingBalance = models.FloatField()
    accountTypeId = models.IntegerField()
    accountType = models.CharField(max_length=255)
    active = models.BooleanField()
    createdBy = models.CharField(max_length=255)
    openOn = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'account'


class AccountCategory(models.Model):
    name = models.CharField(max_length=255)
    accountId = models.IntegerField()
     
    class Meta:
        db_table = 'accountCategory'


class TransactionHistory(models.Model):
    transId = models.CharField(max_length=255)
    transDate = models.CharField(max_length=255)
    transAmount = models.FloatField()
    senderName = models.CharField(max_length=255, blank=True)
    senderAccount = models.CharField(max_length=255, blank=True)
    receiverName = models.CharField(max_length=255, blank=True)
    receiverAccount = models.CharField(max_length=255, blank=True)
    comment = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'transaction_history'


class Teller(models.Model):
    user_id = models.IntegerField()
    tellerId = models.CharField(max_length=100)
    tellerName = models.CharField(max_length=255)

    class Meta:
        db_table = 'teller'


class TellerBalance(models.Model):
    user_id = models.IntegerField()
    tellerId = models.CharField(max_length=100)
    openDate = models.CharField(max_length=100)
    openBal = models.FloatField()
    bal = models.FloatField(default='0')
    closeDate = models.CharField(max_length=100, blank=True)
    closeBal = models.FloatField(default='0')
    totaltran = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=100, default='open')

    class Meta:
        db_table = 'teller_balance'


class TellerTransactionHistory(models.Model):
    user_id = models.IntegerField()
    tellerId = models.CharField(max_length=100)
    transAmount = models.FloatField()
    transAccount = models.CharField(max_length=100)
    transType = models.CharField(max_length=100)
    transDate = models.CharField(max_length=100)
    tellerName = models.CharField(max_length=255)


    class Meta:
        db_table = 'teller_transaction_history'


class LoanApplication(models.Model):
    loanId = models.CharField(max_length=255)
    customerId = models.CharField(max_length=255)
    accountNumber = models.CharField(max_length=255)
    customerName = models.TextField()
    loanAmount = models.FloatField()
    dateApply = models.CharField(max_length=255)
    loanOfficer = models.CharField(max_length=255)
    loanType = models.CharField(max_length=255)
    loanBal = models.FloatField()
    loanStatus = models.CharField(max_length=255)
    dateApprove = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'loan_appliaction'


class Twilio(models.Model):
    smsName = models.TextField(default='twilio')
    account_sid = models.TextField()
    auth_token = models.TextField()

    class Meta:
        db_table = 'twilio'
