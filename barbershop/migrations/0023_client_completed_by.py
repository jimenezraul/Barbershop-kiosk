# Generated by Django 2.2.6 on 2020-04-13 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('barbershop', '0022_client_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='completed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='barbershop.Barbers'),
        ),
    ]
