# Generated by Django 4.0.4 on 2024-03-01 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_companyaddress_companyregistrationdetails_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminCompany',
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
                ('company_admin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='administered_companies', to='crm.employee')),
            ],
        ),
        migrations.AlterField(
            model_name='companyaddress',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='crm.admincompany'),
        ),
        migrations.AlterField(
            model_name='companyregistrationdetails',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registration_details', to='crm.admincompany'),
        ),
        migrations.AlterField(
            model_name='locationregistrationdetails',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location_registration_details', to='crm.admincompany'),
        ),
        migrations.DeleteModel(
            name='Company',
        ),
    ]
