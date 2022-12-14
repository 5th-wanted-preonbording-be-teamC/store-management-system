# Generated by Django 4.1.2 on 2022-10-27 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_user_address"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[],
        ),
        migrations.RemoveField(
            model_name="user",
            name="first_name",
        ),
        migrations.RemoveField(
            model_name="user",
            name="last_name",
        ),
        migrations.AddField(
            model_name="user",
            name="user_name",
            field=models.CharField(
                default="test", max_length=30, verbose_name="사용자 이름"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="user",
            name="password",
            field=models.CharField(max_length=20, verbose_name="비밀번호"),
        ),
    ]
