# Generated by Django 5.0 on 2024-01-10 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('side_bets', '0010_alter_fantasyleague_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='nflseason',
            name='year',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='nflseason',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
