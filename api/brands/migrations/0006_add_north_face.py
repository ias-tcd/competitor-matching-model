# Generated by Django 5.0.3 on 2024-03-27 23:00

from django.db import migrations


def add_north_face(apps, schema_editor):
    brand = apps.get_model("brands", "Brand")
    db_alias = schema_editor.connection.alias
    brand.objects.using(db_alias).create(
        name="North Face",
        logo="https://logos-world.net/wp-content/uploads/2020/11/The-North-Face-Logo-700x394.png",
    )


class Migration(migrations.Migration):
    dependencies = [
        ("brands", "0005_add_nike"),
    ]

    operations = [migrations.RunPython(add_north_face)]
