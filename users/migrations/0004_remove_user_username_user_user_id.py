# Generated by Django 4.1.2 on 2022-10-27 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_alter_user_managers_remove_user_first_name_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="username",
        ),
        migrations.AddField(
            model_name="user",
            name="user_id",
            field=models.CharField(default=False, max_length=20, unique=True),
        ),
    ]
