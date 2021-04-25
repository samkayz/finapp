from django.db.models import fields
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from .models import *
from finappservice.models import *


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = '__all__'


# class RoleCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Role
#         fields = "__all__"


class BranchCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"



class AddresstableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addresstable
        fields =  ['addressLine', 'street', 'landmark', 'country', 'state', 'district', 'mobileNo']



class IdentificationIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdentificationId
        fields = ['modeOfId', 'idNo']


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['customerId', 'mnemonic', 'accounNumber', 'previousBalance', 'workingBalance', 'accountType', 'active']


class ViewCustomerAccountsSerializer(serializers.ModelSerializer):
    account = AccountSerializer(many=True)

    class Meta:
        model = Customer
        fields = ['customerId', 'firstname', 'lastname', 'branchcode', 'account']


# class AccountFilter(serializers.ModelSerializer):
#     class Meta:
#         model = Account
#         fields = ['customerId', 'mnemonic', 'accounNumber', 'previousBalance', 'workingBalance', 'accountType', 'active']

class CustomerSerializer(serializers.ModelSerializer):
    address = AddresstableSerializer(many=True)
    ModeOfId = IdentificationIdSerializer(many=True)
    account = AccountSerializer(many=True)
    class Meta:
        model = Customer
        fields = ['id', 'branchcode', 'customerId', 'firstname', 'lastname', 'mnemonic', 'activationDate', 'submittedDate', 'active', 'address', 'ModeOfId', 'account']


class AccountCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = "__all__"



class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = "__all__"


class TellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teller
        fields = "__all__"


class TellerBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TellerBalance
        fields = "__all__"


class TellerTransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TellerTransactionHistory
        fields = "__all__"


class LoanApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = "__all__"


class TwilioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Twilio
        fields = "__all__"


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'last_login', 'is_superuser', 
        'username', 'email', 'staffname', 'staffid', 
        'is_staff', 'date_joined', 'is_active', 
        'is_teller', 'is_customer_service', 'is_head_teller']
        


class InternalAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternalAccount
        fields = "__all__"


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"