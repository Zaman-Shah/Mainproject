# Generated by Django 4.1.9 on 2023-06-05 04:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0007_remove_patient_pid"),
    ]

    operations = [
        migrations.AlterModelTable(name="patient", table="Patient",),
    ]