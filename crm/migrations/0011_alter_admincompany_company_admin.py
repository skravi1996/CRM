# Generated by Django 4.0.4 on 2024-03-01 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0010_employee_is_company_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admincompany',
            name='company_admin',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='administered_companies', to='crm.employee'),
        ),
    ]
