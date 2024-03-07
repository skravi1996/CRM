# Generated by Django 4.0.4 on 2024-03-01 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_alter_employee_refrence_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='is_staff',
            new_name='completed_now',
        ),
        migrations.RenameField(
            model_name='employee',
            old_name='is_superuser',
            new_name='is_admin',
        ),
        migrations.AddField(
            model_name='employee',
            name='manager',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
