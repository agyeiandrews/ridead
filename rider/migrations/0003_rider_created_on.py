# Generated by Django 5.1.2 on 2024-11-01 20:05

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rider", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="rider",
            name="created_on",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
