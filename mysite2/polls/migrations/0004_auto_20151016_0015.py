# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20151016_0008'),
    ]

    operations = [
        migrations.RenameField(
            model_name='part',
            old_name='part_of',
            new_name='thing',
        ),
    ]
