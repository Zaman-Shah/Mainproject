# Generated by Django 4.1.9 on 2023-06-05 05:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0012_alter_patient_table"),
    ]

    operations = [
        migrations.AlterModelTable(name="patient", table="bot_patient",),
    ]
