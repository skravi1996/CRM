# Generated by Django 4.0.4 on 2024-03-04 05:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0011_alter_admincompany_company_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminComp_Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_type', models.CharField(choices=[('Registered', 'Registered'), ('Headquarters', 'Headquarters'), ('Branch', 'Branch')], max_length=50)),
                ('primary_location', models.BooleanField(default=False)),
                ('address_line1', models.CharField(max_length=255)),
                ('address_line2', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('pin_code', models.CharField(max_length=20)),
                ('district', models.CharField(blank=True, max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='crm.admincompany')),
            ],
        ),
        migrations.DeleteModel(
            name='CompanyAddress',
        ),
    ]
