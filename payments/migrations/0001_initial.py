# Generated by Django 4.1.2 on 2022-10-27 12:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Method",
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
                    "type",
                    models.CharField(
                        choices=[("card", "신용카드"), ("deposit", "무통장입금")],
                        max_length=8,
                        verbose_name="type",
                    ),
                ),
                ("company", models.CharField(max_length=20)),
                ("number", models.CharField(max_length=20)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Payment",
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
                ("price", models.PositiveIntegerField()),
                ("delivery_fee", models.PositiveIntegerField()),
                ("amount", models.PositiveIntegerField()),
                ("delivery_address", models.TextField(blank=True, null=True)),
                ("successed_at", models.DateTimeField(null=True)),
                ("canceled_at", models.DateTimeField(null=True)),
                ("shiped_at", models.DateTimeField(null=True)),
                ("deliveried_at", models.DateTimeField(null=True)),
                (
                    "payment_method",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="payments.method",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="products.product",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]