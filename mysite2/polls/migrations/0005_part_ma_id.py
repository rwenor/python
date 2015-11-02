# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20151016_0015'),
    ]

    operations = [
        migrations.AddField(
            model_name='part',
            name='ma_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
