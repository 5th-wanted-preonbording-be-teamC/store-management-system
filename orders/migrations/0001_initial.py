# Generated by Django 4.1.2 on 2022-10-27 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Order",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("payed", "결제완료"),
                            ("sent", "발송완료"),
                            ("arrived", "배송완료"),
                        ],
                        default="payed",
                        max_length=7,
                        verbose_name="상태",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
