# Generated by Django 4.0.4 on 2022-06-01 05:25

import core.common.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sources', '0029_source_autoid_concept_external_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='autoid_concept_external_id_start_from',
            field=models.IntegerField(default=1, validators=[core.common.validators.validate_non_negative]),
        ),
        migrations.AddField(
            model_name='source',
            name='autoid_concept_mnemonic_start_from',
            field=models.IntegerField(default=1, validators=[core.common.validators.validate_non_negative]),
        ),
        migrations.AddField(
            model_name='source',
            name='autoid_mapping_external_id_start_from',
            field=models.IntegerField(default=1, validators=[core.common.validators.validate_non_negative]),
        ),
        migrations.AddField(
            model_name='source',
            name='autoid_mapping_mnemonic_start_from',
            field=models.IntegerField(default=1, validators=[core.common.validators.validate_non_negative]),
        ),
    ]