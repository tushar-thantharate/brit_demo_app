# Generated by Django 3.2.8 on 2024-01-27 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Products",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=1024, verbose_name="product_name"),
                ),
                ("price", models.IntegerField(verbose_name="product_price")),
            ],
        ),
    ]
