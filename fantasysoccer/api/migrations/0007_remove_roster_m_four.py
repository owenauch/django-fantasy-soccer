# Generated by Django 2.0 on 2018-01-24 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_matchweek_week_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roster',
            name='m_four',
        ),
    ]
