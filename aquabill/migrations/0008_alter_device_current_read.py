# Generated by Django 4.2.8 on 2024-03-15 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("aquabill", "0007_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="device",
            name="current_read",
            field=models.FloatField(null=True),
        ),
    ]
