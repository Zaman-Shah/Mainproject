# Generated by Django 4.1.9 on 2023-06-21 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="history",
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
                ("symptoms", models.TextField(max_length=200)),
                ("tests", models.TextField(max_length=200)),
                ("advise", models.TextField(max_length=200)),
                ("medicine", models.TextField(max_length=200)),
            ],
        ),
    ]