# Generated by Django 5.1.2 on 2024-11-07 17:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("rider", "0002_alter_rider_rider_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="rider",
            old_name="user",
            new_name="user_id",
        ),
    ]
