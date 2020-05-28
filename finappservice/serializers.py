from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from .models import *
from finappservice.models import *


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = '__all__'


class RoleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class OfficeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class AddresstableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addresstable
        fields = "__all__"


class IdentificationIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdentificationId
        fields = "__all__"

class AccountCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountCategory
        fields = "__all__"


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
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