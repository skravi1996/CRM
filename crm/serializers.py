from rest_framework import serializers
from .models import Employee, AdminCompany, AdminComp_Location,Contact_Comp_Address,Contact_comp_Location_RegistrationDetails,Contact_Comp_RegistrationDetails,ContactCompany,Contact, Contact_Address, Contact_Email, Mobile, Landline, Relationship, SignificantDate,Leads, FollowUp

from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        is_staff = validated_data.pop('is_staff', True)
        user = User.objects.create_user(**validated_data, is_staff=is_staff)
        return user
    


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminComp_Location
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, read_only=True)

    class Meta:
        model = AdminCompany
        fields = ['id', 'logo', 'company_name', 'type', 'group', 'website', 'sales_turnover', 'num_employees', 'industry_type', 'industry_sub_type', 'locations']

    def validate(self, data):
        # Check if company name already exists
        company_name = data.get('company_name')
        if AdminCompany.objects.filter(company_name=company_name).exists():
            raise serializers.ValidationError("Company with this name already exists.")
        return data
    


class Contact_Comp_AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact_Comp_Address
        exclude = ('company',)  # Exclude the 'company' field

class Contact_Comp_RegistrationDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact_Comp_RegistrationDetails
        exclude = ('company',)  # Exclude the 'company' field

class Contact_comp_Location_RegistrationDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact_comp_Location_RegistrationDetails
        fields = '__all__'

class ContactCompanySerializer(serializers.ModelSerializer):
    addresses = Contact_Comp_AddressSerializer(many=True)
    registration_details = Contact_Comp_RegistrationDetailsSerializer(many=True)

    class Meta:
        model = ContactCompany
        fields = '__all__'

    def create(self, validated_data):
        addresses_data = validated_data.pop('addresses', [])
        registration_details_data = validated_data.pop('registration_details', [])

        company = ContactCompany.objects.create(**validated_data)

        for address_data in addresses_data:
            Contact_Comp_Address.objects.create(company=company, **address_data)

        for reg_data in registration_details_data:
            location_reg_details_data = reg_data.pop('location_registration_details', [])
            reg_details = Contact_Comp_RegistrationDetails.objects.create(company=company, **reg_data)
            for loc_reg_data in location_reg_details_data:
                Contact_comp_Location_RegistrationDetails.objects.create(company=company, registration_type=reg_details, **loc_reg_data)
        
        return company
    
class MobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mobile
        fields = '__all__'

class LandlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Landline
        fields = '__all__'

class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = '__all__'

class SignificantDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignificantDate
        fields = '__all__'

class ContactAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact_Address
        fields = '__all__'

class ContactEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact_Email
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    emails = ContactEmailSerializer(many=True, read_only=True)
    mobiles = MobileSerializer(many=True, read_only=True)
    addresses = ContactAddressSerializer(many=True, read_only=True)
    landlines = LandlineSerializer(many=True, read_only=True)
    relationships = RelationshipSerializer(many=True, read_only=True)
    significant_dates = SignificantDateSerializer(many=True, read_only=True)

    class Meta:
        model = Contact
        fields = '__all__'
    

class FollowUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUp
        fields = '__all__'

class LeadsSerializer(serializers.ModelSerializer):
    follow_ups = FollowUpSerializer(many=True, read_only=True)
    class Meta:
        model = Leads
        fields = ['id','lead_date', 'lead_status', 'requirement', 'requirement_attachment', 'lead_source', 'contact_person', 'primary_lead_creator', 'lead_assigned_to','follow_ups']
    
    def get_filtered_contact_person_queryset(self):
        user = self.context['request'].user
        employee = Employee.objects.get(email=user.email)  # Assuming Employee model is used for login
        queryset = Contact.objects.filter(associated_company__created_by=employee)
        return queryset
    def get_filtered_lead_assigned_to_queryset(self):
        user = self.context['request'].user
        #employee = Employee.objects.get(email=user.email)
        # Assuming there is a ForeignKey field in Leads model called lead_assigned_to
        queryset = Employee.objects.filter(refrence_id_id=user.id)  # Or whatever logic you need
        return queryset

    def get_fields(self):
        fields = super().get_fields()
        if 'contact_person' in fields:
            fields['contact_person'].queryset = self.get_filtered_contact_person_queryset()
        if 'lead_assigned_to' in fields:
            fields['lead_assigned_to'].queryset = self.get_filtered_lead_assigned_to_queryset()
        return fields

    
    