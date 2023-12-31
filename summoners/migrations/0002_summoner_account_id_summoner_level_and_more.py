# Generated by Django 5.0 on 2023-12-09 05:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("summoners", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="summoner",
            name="account_id",
            field=models.CharField(default=1, max_length=200, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="summoner",
            name="level",
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name="summoner",
            name="profile_icon",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="summoner",
            name="summoner_id",
            field=models.CharField(default=1, max_length=200, unique=True),
            preserve_default=False,
        ),
    ]
