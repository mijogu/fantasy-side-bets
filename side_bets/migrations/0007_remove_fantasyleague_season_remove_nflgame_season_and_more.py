# Generated by Django 5.0 on 2023-12-31 20:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('side_bets', '0006_rename_game_date_nflgame_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fantasyleague',
            name='season',
        ),
        migrations.RemoveField(
            model_name='nflgame',
            name='season',
        ),
        migrations.AlterField(
            model_name='nflgame',
            name='away_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='away_games', to='side_bets.nflteam'),
        ),
        migrations.AlterField(
            model_name='nflgame',
            name='home_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='home_games', to='side_bets.nflteam'),
        ),
    ]
