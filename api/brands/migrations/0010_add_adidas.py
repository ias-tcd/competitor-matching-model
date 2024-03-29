# Generated by Django 5.0.3 on 2024-03-27 22:59

from django.db import migrations


def add_adidas(apps, schema_editor):
    brand = apps.get_model("brands", "Brand")
    db_alias = schema_editor.connection.alias
    brand.objects.using(db_alias).create(
        name="Adidas",
        logo="https://logos-world.net/wp-content/uploads/2020/04/Adidas-Logo-700x394.png",
    )


class Migration(migrations.Migration):
    dependencies = [
        ("brands", "0009_add_under_armour"),
    ]

    operations = [migrations.RunPython(add_adidas)]
