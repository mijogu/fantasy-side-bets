# Generated by Django 5.0 on 2024-01-11 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('side_bets', '0012_alter_fantasyrosterweek_league_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nflgame',
            name='scores_imported',
        ),
        migrations.AddField(
            model_name='nflgame',
            name='are_scores_imported',
            field=models.BooleanField(default=False),
        ),
    ]