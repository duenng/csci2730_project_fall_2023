# Generated by Django 5.0 on 2023-12-09 11:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ui", "0004_alter_votingoption_vote_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="votingoption",
            name="vote_title",
            field=models.CharField(default="None", max_length=200),
            preserve_default=False,
        ),
    ]