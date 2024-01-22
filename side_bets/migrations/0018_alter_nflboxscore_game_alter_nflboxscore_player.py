# Generated by Django 5.0 on 2024-01-12 21:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('side_bets', '0017_alter_nflboxscore_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nflboxscore',
            name='game',
            field=models.ForeignKey(db_constraint=False, db_index=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='boxscores', to='side_bets.nflgame'),
        ),
        migrations.AlterField(
            model_name='nflboxscore',
            name='player',
            field=models.ForeignKey(db_constraint=False, db_index=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='boxscores', to='side_bets.nflplayer', to_field='espn_id'),
        ),
    ]