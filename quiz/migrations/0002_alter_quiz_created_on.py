# Generated by Django 5.0.7 on 2024-08-11 11:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quiz",
            name="created_on",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 8, 11, 16, 56, 31, 623603)
            ),
        ),
    ]
