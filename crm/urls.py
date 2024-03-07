from django.urls import path
from .views import EmployeeListCreateAPIView, EmployeeDetailAPIView, CompanyListCreateAPIView, CompanyDetailAPIView,UserRegistrationAPIView,LoginAPIView,LogoutAPIView,ContactCompanyListCreateAPIView,ContactListCreateAPIView,LeadsCreateAPIView

urlpatterns = [
    path('employees/', EmployeeListCreateAPIView.as_view(), name='employee-list-create'),
    path('employees/<int:pk>/', EmployeeDetailAPIView.as_view(), name='employee-detail'),
    path('companies/', CompanyListCreateAPIView.as_view(), name='company-list-create'),
    path('companies/<int:pk>/', CompanyDetailAPIView.as_view(), name='company-detail'),

    path('ContactCompRegistration/',ContactCompanyListCreateAPIView.as_view(),name='ContactCompRegistration'),
    path('create_contact/',ContactListCreateAPIView.as_view(),name="Create-Contact"),

    path('leads-followups/', LeadsCreateAPIView.as_view(), name='leads-followups-list-create'),
    #path('addresses/', AddressListCreateAPIView.as_view(), name='address-list-create'),
    #path('addresses/<int:pk>/', AddressDetailAPIView.as_view(), name='address-detail'),
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('login/',LoginAPIView.as_view(),name='user-login'),
    path('logout/',LogoutAPIView.as_view(),name='user-logout'),
    

]
