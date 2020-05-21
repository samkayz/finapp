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
    ledgerBalance = models.FloatField()
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


    