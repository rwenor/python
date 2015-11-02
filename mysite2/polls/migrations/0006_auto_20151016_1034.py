# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_part_ma_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='part',
            name='ma_id',
            field=models.IntegerField(default=0),
        ),
    ]
