# Generated by Django 2.2.4 on 2019-08-15 22:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20190815_0040'),
    ]

    operations = [
        migrations.AddField(
            model_name='paypalaccount',
            name='expire',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='paypalaccount',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='paypalaccount', to=settings.AUTH_USER_MODEL),
        ),
    ]
