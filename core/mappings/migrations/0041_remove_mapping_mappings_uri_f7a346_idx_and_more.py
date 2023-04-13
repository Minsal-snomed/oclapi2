# Generated by Django 4.1.7 on 2023-04-13 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mappings', '0040_remove_mapping_mappings_updated_4589ad_idx_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='mapping',
            name='mappings_uri_f7a346_idx',
        ),
        migrations.AlterField(
            model_name='mapping',
            name='uri',
            field=models.TextField(blank=True, null=True),
        ),
    ]
