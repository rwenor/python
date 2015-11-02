# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20151016_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='part',
            name='ma_id',
            field=models.ForeignKey(default=0, to='polls.Ma_Part'),
        ),
    ]
