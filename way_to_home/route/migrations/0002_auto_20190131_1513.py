# Generated by Django 2.1.4 on 2019-01-31 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('route', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='route',
            name='transport_id',
        ),
        migrations.AddField(
            model_name='route',
            name='transport_name',
            field=models.CharField(blank=True, max_length=5),
        ),
    ]
