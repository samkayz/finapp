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

class CustomerSerializer(serializers.ModelSerializer):
    address = AddresstableSerializer(many=True)
    ModeOfId = IdentificationIdSerializer(many=True)
    class Meta:
        model = Customer
        fields = ['id', 'branchcode', 'customerId', 'firstname', 'lastname', 'mnemonic', 'activationDate', 'submittedDate', 'active', 'address', 'ModeOfId']


class AccountCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = "__all__"


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"


class ViewCustomerAccountsSerializer(serializers.ModelSerializer):
    account = AccountSerializer(many=True)

    class Meta:
        model = Customer
        fields = ['customerId', 'firstname', 'lastname', 'branchcode', 'account']


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