from django.contrib import admin
from .models import Employee,AdminCompany,AdminComp_Location,ContactCompany,Contact_Comp_Address,Contact_Comp_RegistrationDetails,Contact_comp_Location_RegistrationDetails,Contact, Contact_Address, Contact_Email, Mobile, Landline, Relationship, SignificantDate,Leads,FollowUp


# Register your models here.
#admin.site.register(Employee)
admin.site.register(AdminCompany)
admin.site.register(AdminComp_Location)

class EmployeeRegistrationDetailsAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'mobile_no', 'refrence_id')

admin.site.register(Employee, EmployeeRegistrationDetailsAdmin)

admin.site.register(ContactCompany)
admin.site.register(Contact_Comp_Address)
admin.site.register(Contact_Comp_RegistrationDetails)
admin.site.register(Contact_comp_Location_RegistrationDetails)

admin.site.register(Contact)
admin.site.register(Contact_Address)
admin.site.register(Contact_Email)
admin.site.register(Mobile)
admin.site.register(Landline)
admin.site.register(Relationship)
admin.site.register(SignificantDate)
admin.site.register(Leads)
admin.site.register(FollowUp)