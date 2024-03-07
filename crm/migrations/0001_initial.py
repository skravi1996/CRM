# Generated by Django 4.0.4 on 2024-02-28 11:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_type', models.CharField(choices=[('EMPLOYEE', 'Employee'), ('COMPANY', 'Company')], default='EMPLOYEE', max_length=20)),
                ('primary_address', models.BooleanField(default=False)),
                ('address_line1', models.CharField(max_length=255)),
                ('address_line2', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('pin_code', models.CharField(max_length=20)),
                ('district', models.CharField(blank=True, max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='company_logos/')),
                ('company_name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('group', models.CharField(blank=True, max_length=100)),
                ('website', models.URLField(blank=True)),
                ('sales_turnover', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('num_employees', models.PositiveIntegerField(blank=True, null=True)),
                ('industry_type', models.CharField(blank=True, max_length=100)),
                ('industry_sub_type', models.CharField(blank=True, max_length=100)),
                ('associated_person', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('mobile_no', models.CharField(max_length=15)),
                ('designation', models.CharField(blank=True, max_length=100)),
                ('grade', models.CharField(max_length=100)),
                ('department', models.CharField(blank=True, max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
