# Generated by Django 2.2.6 on 2020-03-02 05:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photocrop', '0005_auto_20200302_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]