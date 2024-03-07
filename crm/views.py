from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Employee, AdminCompany, AdminComp_Location,ContactCompany,Contact, Contact_Address, Contact_Email, Mobile, Landline, Relationship, SignificantDate,Leads
from .serializers import EmployeeSerializer, CompanySerializer, LocationSerializer,UserSerializer,ContactCompanySerializer,ContactSerializer, ContactAddressSerializer, ContactEmailSerializer, MobileSerializer, LandlineSerializer, RelationshipSerializer, SignificantDateSerializer,LeadsSerializer, FollowUpSerializer
#from rest_framework.permissions import IsAdminUser
from .permissions import IsEmployeeAdmin,IsEmployeeAdminOrSelf,IsCompanyAdmin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from rest_framework.authtoken.models import Token
from django.http import Http404
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework import generics


class UserRegistrationAPIView(APIView):
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            # Save the user
            user = user_serializer.save(username=request.data.get('email'))

            # Construct the full_name for the Employee record
            first_name = request.data.get('first_name', '')
            last_name = request.data.get('last_name', '')
            middle_name = request.data.get('middle_name', '')
            #password = request.data.get('password', '')

            full_name_parts = [first_name]
            if middle_name:
                full_name_parts.append(middle_name)
            if last_name:
                full_name_parts.append(last_name)

            full_name = ' '.join(full_name_parts)

            # Create an employee record associated with the user
            employee_data = {
                'full_name': full_name,
                'email': request.data.get('email'),
                'mobile_no': request.data.get('mobile_no'),
                'refrence_id': user.id,  # Associate the employee record with the newly created user
                'is_admin': request.data.get('is_admin', True),  # Optionally, get is_staff from request data
                'is_company_admin': True  # Optionally, get is_superuser from request data
            }
            employee_serializer = EmployeeSerializer(data=employee_data)
            if employee_serializer.is_valid():
                # Save the employee record
                employee_serializer.save()
                user = authenticate(username=user.username, password=request.data.get('password', ''))
                if user is not None:
                    login(request, user)

                return Response("User registered and logged in successfully", status=status.HTTP_201_CREATED)
            else:
                # If there's an error in employee data, delete the created user
                user.delete()
                return Response(employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else: 
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):
        # Get username and password from request data
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(username=username, password=password)

        # Check if authentication was successful
        if user is not None:
            login(request, user)
            # User successfully authenticated
            try:
                employee = Employee.objects.get(email=request.user.email)
                #employee = Employee.objects.get(refrence_id=user)
                
                full_name = employee.full_name
                print(full_name)
            except Employee.DoesNotExist:
                full_name = None
            return Response({
                'msg': 'User successfully logged in',
                'full_name': full_name,  # Retrieve full name
                'email': user.email,  # Retrieve email
            }, status=status.HTTP_200_OK)
        else:
            # Authentication failed
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class LogoutAPIView(APIView):
    def post(self, request):
        # Logout the user
        logout(request)
        return Response({'msg': 'User successfully logged out'}, status=status.HTTP_200_OK)
        
# Registed by Company admin
class EmployeeListCreateAPIView(APIView):
    permission_classes = [IsEmployeeAdmin]
    def get(self, request):
        employee = Employee.objects.get(email=request.user.email)
        print(employee.refrence_id)
        employees = Employee.objects.filter(refrence_id=employee.refrence_id)

        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        employee = Employee.objects.get(email=request.user.email)
        print(request.data)
        if serializer.is_valid():
            user = User(
            username=request.data.get('email'),  # Use email as username
            email=request.data.get('email'),
            is_staff=request.data.get('is_admin', False),
            #is_superuser=request.data.get('is_superuser', False)
            )
            user.set_password('12345')  # Set default password
            user.save()  
            serializer.save(refrence_id=employee.refrence_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetailAPIView(APIView):
    permission_classes = [IsEmployeeAdminOrSelf]

    def get_object(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee, context={'request': request})  # Pass request context here
        return Response(serializer.data)

    def put(self, request, pk):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee, data=request.data, context={'request': request})  # Pass request context here
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        employee = self.get_object(pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CompanyListCreateAPIView(APIView):
    permission_classes = [IsCompanyAdmin]

    def get(self, request):
        employee = Employee.objects.get(email=request.user.email)
        companies = AdminCompany.objects.filter(company_admin=employee.id)
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

    def post(self, request):
        company_data = request.data.copy()
        employee = Employee.objects.get(email=request.user.email)
        print(employee.email)
        # Assign the employee instance to the company_admin field
        #request.data['company_admin'] = company_admin.id
        company_serializer = CompanySerializer(data=request.data)
        try:
            if company_serializer.is_valid():
                company=company_serializer.save(company_admin=employee)
                locations_data = company_data.pop('locations', [])
                for location_data in locations_data:
                    location_data['company'] = company.id  # Set the company ID for the location
                    location_serializer = LocationSerializer(data=location_data)
                    if location_serializer.is_valid():
                        location_serializer.save()  # Save the location
                    else:
                        # Rollback the company creation if any location is invalid
                        company.delete()
                        return Response(location_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                return Response(company_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(company_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({"error": "Your Company already exists."}, status=status.HTTP_400_BAD_REQUEST)

class CompanyDetailAPIView(APIView):
    permission_classes = [IsCompanyAdmin]
    
    def get_object(self, pk):
        try:
            return AdminCompany.objects.get(pk=pk)
        except AdminCompany.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        company = self.get_object(pk)
        print(company.company_admin.is_company_admin)
        if company.company_admin.is_company_admin and  company.company_admin.email != request.user.email:
            return Response({'error': 'You do not have permission to update this company.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    def put(self, request, pk):
        company = self.get_object(pk)
        
        # Check if the logged-in user is the company admin for the requested company
        if company.company_admin.is_company_admin and  company.company_admin.email != request.user.email:
            return Response({'error': 'You do not have permission to update this company.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Update company locations if provided in the request
            locations_data = request.data.get('locations', [])
            for location_data in locations_data:
                location_id = location_data.get('id')
                if location_id:
                    # If location ID is provided, update the existing location
                    location = AdminComp_Location.objects.get(id=location_id)
                    location_serializer = LocationSerializer(location, data=location_data)
                else:
                    # If no location ID is provided, create a new location
                    location_data['company'] = company.id
                    location_serializer = LocationSerializer(data=location_data)
                if location_serializer.is_valid():
                    location_serializer.save()
                else:
                    return Response(location_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        company = self.get_object(pk)
        
        # Check if the logged-in user is the company admin for the requested company
        if company.company_admin.is_company_admin and  company.company_admin.email != request.user.email:
            return Response({'error': 'You do not have permission to delete this company.'}, status=status.HTTP_403_FORBIDDEN)
        
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class ContactCompanyListCreateAPIView(APIView):
    def get(self, request):
        employee = Employee.objects.get(email=request.user.email)
        print(employee.refrence_id_id)
        
        companies = ContactCompany.objects.filter(created_by__refrence_id_id=employee.refrence_id_id)
        serializer = ContactCompanySerializer(companies, many=True)
        return Response(serializer.data)

    def post(self, request):
        employee = Employee.objects.get(email=request.user.email)
        print(employee.id)
        request.data['created_by'] = employee.id
        serializer = ContactCompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#ContactCompanyDetailsAPIView





class ContactListCreateAPIView(APIView):
    def get(self, request):
        employee = Employee.objects.get(email=request.user.email)
        print(employee.refrence_id_id)

        contacts = Contact.objects.filter(associated_company__created_by__refrence_id=request.user.id)
        #a=Contact.objects.first()
        #print(a)
        #print(a.associated_company.created_by.refrence_id_id)
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    def post(self, request):
        associated_company_id = request.data.get('associated_company')
        if associated_company_id is not None:
            associated_company = get_object_or_404(ContactCompany, pk=associated_company_id)
            print(associated_company.created_by.refrence_id_id,request.user.id)
            if associated_company.created_by.refrence_id_id != request.user.id:
                raise ValidationError("Associated company does not belong to the logged-in user.")
        contact_data = request.data
        addresses_data = contact_data.pop('addresses', [])
        emails_data = contact_data.pop('emails', [])
        mobiles_data = contact_data.pop('mobiles', [])
        landlines_data = contact_data.pop('landlines', [])
        relationships_data = contact_data.pop('relationships', [])
        significant_dates_data = contact_data.pop('significant_dates', [])

        contact_serializer = ContactSerializer(data=contact_data)
        if contact_serializer.is_valid():
            contact = contact_serializer.save()

            for address_data in addresses_data:
                address_data['contact'] = contact.id
                address_serializer = ContactAddressSerializer(data=address_data)
                if address_serializer.is_valid():
                    address_serializer.save()
                else:
                    contact.delete()  # Delete the contact if address serializer is not valid
                    return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # Create emails
            for email_data in emails_data:
                email_data['contact'] = contact.id
                email_serializer = ContactEmailSerializer(data=email_data)
                if email_serializer.is_valid():
                    email_serializer.save()
                else:
                    contact.delete()  # Delete the contact if address serializer is not valid
                    return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Create mobiles
            for mobile_data in mobiles_data:
                mobile_data['contact'] = contact.id
                mobile_serializer = MobileSerializer(data=mobile_data)
                if mobile_serializer.is_valid():
                    mobile_serializer.save()
                else:
                    contact.delete()  # Delete the contact if address serializer is not valid
                    return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Create landlines
            for landline_data in landlines_data:
                landline_data['contact'] = contact.id
                landline_serializer = LandlineSerializer(data=landline_data)
                if landline_serializer.is_valid():
                    landline_serializer.save()
                else:
                    contact.delete()  # Delete the contact if address serializer is not valid
                    return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Create relationships
            for relationship_data in relationships_data:
                relationship_data['contact'] = contact.id
                relationship_serializer = RelationshipSerializer(data=relationship_data)
                if relationship_serializer.is_valid():
                    relationship_serializer.save()
                else:
                    contact.delete()  # Delete the contact if address serializer is not valid
                    return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Create significant dates
            for significant_date_data in significant_dates_data:
                significant_date_data['contact'] = contact.id
                significant_date_serializer = SignificantDateSerializer(data=significant_date_data)
                if significant_date_serializer.is_valid():
                    significant_date_serializer.save()
                else:
                    contact.delete()  # Delete the contact if address serializer is not valid
                    return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Repeat similar logic for other nested serializers

            return Response(contact_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(contact_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class LeadsCreateAPIView(APIView):
    def get(self, request, format=None):
        employee = Employee.objects.get(email=request.user.email)
        print(employee.refrence_id_id)
        leads = Leads.objects.filter(primary_lead_creator__refrence_id_id=employee.refrence_id_id)
        for i in leads:
            print(i.primary_lead_creator.refrence_id_id)
        serializer = LeadsSerializer(leads, many=True, context={'request': request})
        return Response(serializer.data)

    
    def post(self, request, format=None):
        lead_serializer = LeadsSerializer(data=request.data,context={'request': request})
        if lead_serializer.is_valid():
            employee = Employee.objects.get(email=request.user.email)
            #print(a)
            lead_instance = lead_serializer.save(primary_lead_creator=employee)
            print(lead_instance.id)
            # Retrieve follow-up data from request
            follow_ups_data = request.data.get('follow_ups', [])
            print(follow_ups_data)
            for follow_up_data in follow_ups_data:
                follow_up_data['lead'] = lead_instance.id  # Make sure to include the lead field
                follow_up_serializer = FollowUpSerializer(data=follow_up_data)
                if follow_up_serializer.is_valid():
                    follow_up_serializer.save()
                else:
                    lead_instance.delete()
                    return Response(follow_up_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(lead_serializer.data, status=status.HTTP_201_CREATED)
        return Response(lead_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
