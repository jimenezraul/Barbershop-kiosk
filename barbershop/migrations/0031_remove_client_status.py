# Generated by Django 2.2.6 on 2020-05-28 23:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barbershop', '0030_client_completed_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='status',
        ),
    ]
