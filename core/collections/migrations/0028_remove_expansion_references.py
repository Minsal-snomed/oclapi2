# Generated by Django 3.2.7 on 2021-09-10 03:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collections', '0027_auto_20210830_0634'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expansion',
            name='references',
        ),
    ]