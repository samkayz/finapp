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
]