# Generated by Django 2.1.4 on 2019-01-15 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='end_time',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='notification',
            name='start_time',
            field=models.DateField(),
        ),
    ]
