# Generated by Django 2.2.6 on 2020-03-26 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barbershop', '0013_barbers_hire_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='barbers',
            name='available',
            field=models.BooleanField(default=False),
        ),
    ]
