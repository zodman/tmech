# Generated by Django 2.2.4 on 2019-08-15 05:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0009_auto_20190809_0421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conf',
            name='logo',
            field=models.URLField(help_text='Set url for a image'),
        ),
        migrations.AlterField(
            model_name='conf',
            name='name',
            field=models.CharField(help_text='Company name', max_length=200),
        ),
        migrations.CreateModel(
            name='PaypalAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
