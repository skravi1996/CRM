from django.db import models
from django.contrib.auth.models import User


# Define model for Employee
class Employee(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_no = models.CharField(max_length=15,blank=True)
    designation = models.CharField(max_length=100,blank=True)
    grade = models.CharField(max_length=100,blank=True)
    department = models.CharField(max_length=100, blank=True)
    manager = models.CharField(max_length=100, blank=True)  #ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    #company_name = models.CharField(max_length=200)
    #created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    refrence_id = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    photo = models.ImageField(upload_to='employee_photo/', blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_company_admin=models.BooleanField(default=False)
    completed_now = models.BooleanField(default=False)
    #is_superuser = models.BooleanField(default=False)

    """def save(self, *args, **kwargs):
        user = User.objects.create_user(username=self.email, email=self.email, password='12345', is_staff=self.is_staff)
        super(Employee, self).save(*args, **kwargs)"""

    def __str__(self):
        return self.full_name



class AdminCompany(models.Model):
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    company_name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    group = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    sales_turnover = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    num_employees = models.PositiveIntegerField(blank=True, null=True)
    industry_type = models.CharField(max_length=100, blank=True)
    industry_sub_type = models.CharField(max_length=100, blank=True)
    company_admin = models.OneToOneField(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='administered_companies')

    def __str__(self):
        return self.company_name

class AdminComp_Location(models.Model):
    LOCATION_TYPE_CHOICES = [
        ('Registered', 'Registered'),
        ('Headquarters', 'Headquarters'),
        ('Branch', 'Branch'),
        # Add more choices as needed
    ]
    
    company = models.ForeignKey(AdminCompany, on_delete=models.CASCADE, related_name='locations')
    location_type = models.CharField(max_length=50, choices=LOCATION_TYPE_CHOICES)
    primary_location = models.BooleanField(default=False)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=20)
    district = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.company.company_name} - {self.location_type}"



class ContactCompany(models.Model):
    logo = models.ImageField(upload_to='contact_company_logos/', blank=True, null=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    group = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    sales_turnover = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    num_employees = models.PositiveIntegerField(blank=True, null=True)
    industry_type = models.CharField(max_length=100, blank=True)
    industry_sub_type = models.CharField(max_length=100, blank=True)
    created_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='contact_companies', null=True, blank=True)
    

    def __str__(self):
        return self.name
    
class Contact_Comp_Address(models.Model):
    ADDRESS_TYPE_CHOICES = [
        ('Registered', 'Registered'),
        ('Headquarters', 'Headquarters'),
        ('Branch', 'Branch'),
    ]

    company = models.ForeignKey(ContactCompany, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=50, choices=ADDRESS_TYPE_CHOICES)
    primary_address = models.BooleanField(default=False)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=20)
    district = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.company.name} - {self.address_type}"

class Contact_Comp_RegistrationDetails(models.Model):
    company = models.ForeignKey(ContactCompany, on_delete=models.CASCADE, related_name='registration_details')
    registration_type = models.CharField(max_length=100)
    registration_since = models.DateField(blank=True, null=True)
    registration_number = models.CharField(max_length=100)

class Contact_comp_Location_RegistrationDetails(models.Model):
    company = models.ForeignKey(ContactCompany, on_delete=models.CASCADE, related_name='location_registration_details')
    address_type = models.CharField(max_length=100)
    registration_type = models.CharField(max_length=100)
    registration_since = models.DateField(blank=True, null=True)
    registration_number = models.CharField(max_length=100)



class Contact(models.Model):
    # Personal Information
    photo = models.ImageField(upload_to='contact_photos/', blank=True, null=True)
    title = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    # Associated Company
    associated_company = models.ForeignKey(ContactCompany, on_delete=models.SET_NULL, null=True, blank=True, related_name='contacts')
    # Social Links
    facebook = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    whatsapp = models.URLField(blank=True)
    website = models.URLField(blank=True)
    other_social_link = models.URLField(blank=True)
    
    class Meta:
        verbose_name_plural = "Contacts"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.associated_company.name}"

class Contact_Address(models.Model):
    ADDRESS_TYPE_CHOICES = [
        ('Home', 'Home'),
        ('Work', 'Work'),
        ('Other', 'Other'),
    ]

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=50, choices=ADDRESS_TYPE_CHOICES)
    primary_address = models.BooleanField(default=False)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=20)
    district = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.contact.first_name} {self.contact.last_name} - {self.address_type}"

class Contact_Email(models.Model):
    EMAIL_TYPE_CHOICES = [
        ('Personal', 'Personal'),
        ('Work', 'Work'),
        ('Other', 'Other'),
    ]

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='emails')
    email_type = models.CharField(max_length=50, choices=EMAIL_TYPE_CHOICES)
    primary_email = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.contact.first_name} {self.contact.last_name} - {self.email_type}"

class Mobile(models.Model):
    MOBILE_TYPE_CHOICES = [
        ('Personal', 'Personal'),
        ('Work', 'Work'),
        ('Other', 'Other'),
    ]

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='mobiles')
    mobile_type = models.CharField(max_length=50, choices=MOBILE_TYPE_CHOICES)
    primary_mobile = models.BooleanField(default=False)
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.contact.first_name} {self.contact.last_name} - {self.mobile_type}"

class Landline(models.Model):
    LANDLINE_TYPE_CHOICES = [
        ('Personal', 'Personal'),
        ('Work', 'Work'),
        ('Other', 'Other'),
    ]

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='landlines')
    landline_type = models.CharField(max_length=50, choices=LANDLINE_TYPE_CHOICES)
    primary_landline = models.BooleanField(default=False)
    landline = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.contact.first_name} {self.contact.last_name} - {self.landline_type}"

class Relationship(models.Model):
    RELATIONSHIP_TYPE_CHOICES = [
        ('Family', 'Family'),
        ('Friend', 'Friend'),
        ('Colleague', 'Colleague'),
        ('Other', 'Other'),
    ]

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='relationships')
    relationship_type = models.CharField(max_length=50, choices=RELATIONSHIP_TYPE_CHOICES)
    relationship_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.contact.first_name} {self.contact.last_name} - {self.relationship_type}"


class SignificantDate(models.Model):
    DATE_TYPE_CHOICES = [
        ('Birthday', 'Birthday'),
        ('Anniversary', 'Anniversary'),
        ('Other', 'Other'),
    ]

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='significant_dates')
    date_type = models.CharField(max_length=50, choices=DATE_TYPE_CHOICES)
    date = models.DateField()

    def __str__(self):
        return f"{self.contact.first_name} {self.contact.last_name} - {self.date_type}"
    

#Lead Managements Table
class Leads(models.Model):
    LEAD_STATUS_CHOICES = [
        ('New', 'New'),
        ('Contacted', 'Contacted'),
        ('Converted', 'Converted'),
        ('Closed', 'Closed'),
    ]

    LEAD_SOURCE_CHOICES = [
        ('Website', 'Website'),
        ('Referral', 'Referral'),
        ('Advertisement', 'Advertisement'),
        ('Cold Call', 'Cold Call'),
        ('Other', 'Other'),
    ]
    contact_person = models.ForeignKey('Contact', on_delete=models.SET_NULL, null=True, blank=True)
    lead_date = models.DateField()
    lead_status = models.CharField(max_length=50, choices=LEAD_STATUS_CHOICES)
    requirement = models.TextField()
    requirement_attachment = models.FileField(upload_to='requirement_attachments/', blank=True, null=True)
    lead_source = models.CharField(max_length=100, choices=LEAD_SOURCE_CHOICES)
    primary_lead_creator = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='leads_created')
    lead_assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='leads_assigned_to')
    def __str__(self):
        return f"{self.contact_person}"



class FollowUp(models.Model):
    FOLLOW_UP_TYPE_CHOICES = [
        ('Call', 'Call'),
        ('Meeting', 'Meeting'),
        ('Email', 'Email'),
        ('Other', 'Other'),
    ]
    follow_up_type = models.CharField(max_length=50, choices=FOLLOW_UP_TYPE_CHOICES)
    follow_up_date_and_time = models.DateTimeField()
    follow_up_notes = models.TextField()
    follow_up_attachment = models.FileField(upload_to='follow_up_attachments/', blank=True, null=True)
    lead = models.ForeignKey(Leads, on_delete=models.CASCADE, related_name='follow_ups')
    def __str__(self) -> str:
        return f"{self.lead}"

