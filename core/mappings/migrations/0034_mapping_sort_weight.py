# Generated by Django 4.1.1 on 2022-12-21 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mappings', '0033_mapping_mappings_ver_updated_at_idx_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mapping',
            name='sort_weight',
            field=models.FloatField(blank=True, db_index=True, null=True),
        ),
    ]