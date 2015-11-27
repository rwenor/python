# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_auto_20151016_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mn_name',
            name='mn_Url',
            field=models.CharField(max_length=60),
        ),
    ]
