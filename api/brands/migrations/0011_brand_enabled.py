# Generated by Django 5.0.3 on 2024-04-07 17:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("brands", "0010_add_adidas"),
    ]

    operations = [
        migrations.AddField(
            model_name="brand",
            name="enabled",
            field=models.BooleanField(default=False),
        ),
    ]
