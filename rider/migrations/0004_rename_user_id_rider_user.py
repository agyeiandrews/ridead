# Generated by Django 5.1.2 on 2024-11-07 18:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("rider", "0003_rename_user_rider_user_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="rider",
            old_name="user_id",
            new_name="user",
        ),
    ]
