from django.urls import path, include
from finappservice import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('createUser', views.createUser),
    path('createOffice', views.createOffice),
    path('offices', views.offices),
    path('createCustomer', views.createCustomer),
    path('allCustomer', views.allCustomer),
    path('customerById/<customerId>', views.customerById),
    path('acctCategory', views.acctCategory),
    path('allAcctCategory', views.allAcctCategory),
    path('openAccount', views.openAccount),
    path('customerAccount/<customerId>', views.customerAccount),
    path('fundTransfer', views.fundTransfer),
    path('allTrasaction', views.allTrasaction),
    path('transById/<transId>', views.transById),
    path('assignTeller', views.assignTeller),
    path('openBal', views.openBal),
    path('checkCurrentTellerBal/<telleId>', views.checkCurrentTellerBal),
    path('operate', views.operate),
    path('enquiry', views.enquiry),
    path('closeBal', views.closeBal),
    path('loanApply', views.loanApply),
    path('allLoan', views.allLoan),
    path('approveLoan', views.approveLoan),
    path('smsTwilio', views.smsTwilio),
]