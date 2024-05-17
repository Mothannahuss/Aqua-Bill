# Generated by Django 4.2.8 on 2024-03-03 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("aquabill", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Device",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("last_update", models.DateField(auto_now_add=True)),
                ("current_read", models.FloatField()),
                ("current_month", models.CharField(max_length=9)),
                ("month_read", models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Unit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("url", models.URLField()),
                (
                    "device",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="aquabill.device",
                    ),
                ),
            ],
        ),
    ]
