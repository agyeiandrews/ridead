# Generated by Django 5.1.2 on 2024-11-03 18:33

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0005_alter_user_profile_picture"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="profile_picture",
            field=cloudinary.models.CloudinaryField(
                blank=True, max_length=255, null=True, verbose_name="profile_picture"
            ),
        ),
    ]
