# Generated by Django 5.0.2 on 2024-03-02 19:49

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("requests_app", "0003_alter_request_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="request",
            name="request_location",
            field=django.contrib.gis.db.models.fields.PointField(
                default="Point(31.814492376242235 31.420542367096505)", srid=4326
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="request",
            name="status",
            field=models.CharField(default="Open", max_length=50),
        ),
    ]
