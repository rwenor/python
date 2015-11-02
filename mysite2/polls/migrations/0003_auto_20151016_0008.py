# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_ma_part_part_thing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='part',
            name='ma_id',
        ),
        migrations.AddField(
            model_name='part',
            name='part_of',
            field=models.ForeignKey(default=1, to='polls.Thing'),
            preserve_default=False,
        ),
    ]
