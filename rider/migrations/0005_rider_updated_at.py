# Generated by Django 5.1.2 on 2024-11-07 19:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rider", "0004_rename_user_id_rider_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="rider",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
