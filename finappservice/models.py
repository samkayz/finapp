from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser, UserManager, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.sessions.models import Session




class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(blank=True)
    staffname = models.TextField(verbose_name='staffname', null=True, blank=True)
    staffid = models.TextField(verbose_name='staffid', null=True, blank=True)
    is_staff = models.BooleanField(verbose_name='is_staff', default=True)
    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)
    is_active = models.BooleanField(verbose_name='is_active', default=True)
    is_teller = models.BooleanField(verbose_name='is_teller', default=False)
    is_head_teller = models.BooleanField(verbose_name='is_head_teller', default=False)
    is_customer_service = models.BooleanField(verbose_name='is_customer_service', default=False)

    objects =  UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.username



# class Role(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()

#     class Meta:
#         db_table = 'role'


class Branch(models.Model):
    name = models.CharField(max_length=255)
    branchcode = models.CharField(max_length=255, null=True, blank=True)
    opening_date = models.DateField(auto_now=True)

    class Meta:
        db_table = 'branch'


class Customer(models.Model):
    branchcode = models.CharField(max_length=255, null=True, blank=True)
    customerId = models.CharField(max_length=255, null=True, blank=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    mnemonic = models.CharField(max_length=100)
    activationDate = models.CharField(max_length=255, null=True, blank=True)
    submittedDate = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


    class Meta:
        db_table = 'customer'


class Addresstable(models.Model):
    customer = models.ForeignKey(Customer, related_name='address', on_delete=models.CASCADE)
    addressLine = models.TextField(null=True, blank=True)
    street = models.TextField(null=True, blank=True)
    landmark = models.TextField(null=True, blank=True)
    country = models.TextField(null=True, blank=True)
    state = models.TextField(null=True, blank=True)
    district = models.TextField(null=True, blank=True)
    mobileNo = models.TextField(null=True, blank=True)
    mnemonic = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'addresstable'


class IdentificationId(models.Model):
    customer = models.ForeignKey(Customer, related_name='ModeOfId', on_delete=models.CASCADE)
    modeOfId = models.CharField(max_length=255)
    idNo = models.CharField(max_length=255)
    mnemonic = models.CharField(max_length=255)

    class Meta:
        db_table = 'identification_id'


class AccountType(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateField(auto_now=True)
     
    class Meta:
        db_table = 'account_type'

        
class Account(models.Model):
    customer = models.ForeignKey(Customer, related_name='account', on_delete=models.CASCADE)
    customerId = models.CharField(max_length=255)
    mnemonic = models.CharField(max_length=255)
    accountName = models.TextField()
    accounNumber = models.CharField(max_length=255)
    previousBalance = models.FloatField(default=0)
    workingBalance = models.FloatField(default=0)
    accountTypeId = models.IntegerField()
    accountType = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    createdBy = models.CharField(max_length=255)
    openOn = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'account'




class TransactionHistory(models.Model):
    transId = models.CharField(max_length=255)
    transDate = models.DateTimeField(auto_now=True)
    transAmount = models.FloatField()
    senderName = models.CharField(max_length=255, blank=True)
    senderAccount = models.CharField(max_length=255, blank=True)
    receiverName = models.CharField(max_length=255, blank=True)
    receiverAccount = models.CharField(max_length=255, blank=True)
    comment = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'transaction_history'


class Teller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_head_teller = models.BooleanField(default=False)
    tellerId = models.CharField(max_length=100)
    tellerName = models.CharField(max_length=255)

    class Meta:
        db_table = 'teller'
    

class CustomerService(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staffid = models.CharField(max_length=100)
    staffname = models.CharField(max_length=255)

    class Meta:
        db_table = 'customer_service'


class TellerBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
    teller = models.OneToOneField(User, on_delete=models.CASCADE)
    transAmount = models.FloatField()
    transAccount = models.CharField(max_length=100)
    transType = models.CharField(max_length=100)
    transDate = models.CharField(max_length=100)
    tellerName = models.CharField(max_length=255)


    class Meta:
        db_table = 'teller_transaction_history'


class LoanType(models.Model):
    loan_code = models.TextField(null=True, blank=True)
    loan_name = models.TextField(null=True, blank=True)
    loan_duration = models.BigIntegerField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'loan_type'


class Products(models.Model):
    product_code = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'products'
        

class LoanApplication(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loanId = models.CharField(max_length=255)
    customerId = models.CharField(max_length=255)
    accountNumber = models.CharField(max_length=255)
    customerName = models.TextField()
    loanAmount = models.FloatField()
    dateApply = models.CharField(max_length=255)
    loanOfficer = models.CharField(max_length=255)
    loan_code = models.CharField(max_length=255)
    loanBal = models.FloatField()
    duration = models.BigIntegerField(null=True, blank=True)
    pay_day = models.DateField(null=True, blank=True)
    loan_approve = models.BooleanField(default=False)
    loan_paid = models.BooleanField(default=False)
    dateApprove = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'loan_appliaction'


class Twilio(models.Model):
    smsName = models.TextField(default='twilio')
    account_sid = models.TextField()
    auth_token = models.TextField()

    class Meta:
        db_table = 'twilio'
        
        
class InternalAccount(models.Model):
    product_code = models.TextField(null=True, blank=True)
    product_name = models.TextField(null=True, blank=True)
    account_number = models.TextField(null=True, blank=True)
    prev_bal = models.FloatField(default=0)
    working_bal = models.FloatField(default=0)
    
    class Meta:
        db_table = 'internal_account'
        


class InternalTransactHistory(models.Model):
    product_code = models.TextField(null=True, blank=True)
    txn_id = models.TextField(null=True, blank=True)
    frm_acct = models.TextField(null=True, blank=True)
    to_acct = models.TextField(null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    product_name = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now=True, null=True)
    
    
    class Meta:
        db_table = 'internal_history'
        
        
class Currency(models.Model):
    cur_code = models.CharField(max_length=100)
    cur_name = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        db_table = 'currency'