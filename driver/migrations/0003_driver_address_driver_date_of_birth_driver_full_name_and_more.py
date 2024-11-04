# Generated by Django 5.1.2 on 2024-11-02 21:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("driver", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="driver",
            name="address",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="driver",
            name="date_of_birth",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="driver",
            name="full_name",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="driver",
            name="profile_picture",
            field=models.ImageField(
                blank=True, null=True, upload_to="profile_pictures/"
            ),
        ),
        migrations.AddField(
            model_name="driver",
            name="status",
            field=models.CharField(
                choices=[("active", "Active"), ("inactive", "Inactive")],
                default="active",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="driver",
            name="vehicle_type",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]