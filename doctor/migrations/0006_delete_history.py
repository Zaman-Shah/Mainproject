# Generated by Django 4.1.7 on 2023-07-06 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0005_remove_history_patient_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='history',
        ),
    ]
