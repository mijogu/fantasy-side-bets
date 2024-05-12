# Generated by Django 5.0.2 on 2024-05-11 01:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('side_bets', '0020_remove_nflseason_year_alter_nflseason_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fantasyrosterweek',
            name='league',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='roster_weeks', to='side_bets.fantasyleague'),
        ),
        migrations.AlterField(
            model_name='fantasyrosterweek',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='roster_weeks', to='side_bets.fantasyteam'),
        ),
    ]
