# Generated by Django 5.0 on 2023-12-15 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=200)),
                ('password', models.CharField(max_length=50)),
                ('display_name', models.CharField(max_length=200)),
                ('sleeper_id', models.CharField(max_length=100)),
            ],
        ),
    ]
