# Generated by Django 4.1.9 on 2023-06-02 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0005_alter_patient_age"),
    ]

    operations = [
        migrations.AddField(
            model_name="patient",
            name="pid",
            field=models.IntegerField(default=0, max_length=20),
        ),
    ]
