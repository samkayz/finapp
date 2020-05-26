from django.urls import path, include
from finappservice import views


urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('role', views.role),
    path('createOffice', views.createOffice),
    path('roles', views.roles),
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
]