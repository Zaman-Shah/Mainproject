# Generated by Django 4.1.9 on 2023-06-05 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0014_alter_patient_table"),
    ]

    operations = [
        migrations.CreateModel(
            name="department",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("dept_id", models.IntegerField()),
                ("dname", models.CharField(max_length=100)),
            ],
        ),
    ]
