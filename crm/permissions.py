from rest_framework import permissions
from .models import Employee
class IsEmployeeAdmin(permissions.BasePermission):
    """
    Custom permission to only allow employees with is_staff=True to access the view.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and is_staff is True
        return request.user.is_authenticated and request.user.is_staff 

class IsEmployeeAdminOrSelf(permissions.BasePermission):
    """
    Custom permission to allow admins to access any employee detail,
    and allow employees to access their own detail.
    """
    def has_permission(self, request, view):
        # Check if user is authenticated
        if request.user.is_authenticated:
            # Allow access if user is admin
            if request.user.is_staff:
                return True
            # Allow access if user is trying to access their own detail
            
            employee = Employee.objects.get(email=request.user.email)
            print(str(employee.id))
            if view.kwargs.get('pk') == employee.id:
                return True
        return False

from rest_framework.permissions import BasePermission

class IsCompanyAdmin(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated and is a company admin
        if request.user.is_authenticated:
            try:
                employee = Employee.objects.get(email=request.user.email)
                #print(employee.is_company_admin)
                # Check if the user's employee instance has is_company_admin set to True
                return employee.is_company_admin
            except AttributeError:
                # If there's no associated employee instance, return False
                return False
        return False
