# Generated by Django 2.2.6 on 2020-03-03 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='zip_code',
            field=models.CharField(default='32738', max_length=12),
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='address',
            name='state',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='address',
            name='street',
            field=models.CharField(max_length=100),
        ),
    ]
