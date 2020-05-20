from django.urls import path, include
from finappservice import views


urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('role', views.role),
    path('createOffice', views.createOffice),
    path('roles', views.roles)
]