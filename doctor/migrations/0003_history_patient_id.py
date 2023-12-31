# Generated by Django 4.1.9 on 2023-06-26 05:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_remove_patient_details_ap_date_and_more"),
        ("doctor", "0002_rename_advise_history_advice"),
    ]

    operations = [
        migrations.AddField(
            model_name="history",
            name="patient_id",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                to="accounts.patient_details",
            ),
        ),
    ]
