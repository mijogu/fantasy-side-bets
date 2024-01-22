# Generated by Django 5.0 on 2024-01-12 20:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('side_bets', '0015_nflplayer_number_nflplayer_rotowire_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nflboxscore',
            name='player',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='boxscores', to='side_bets.nflplayer', to_field='espn_id'),
        ),
    ]
