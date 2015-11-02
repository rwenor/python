# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_auto_20151016_1039'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mn_Name',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mn_Name', models.CharField(max_length=20)),
                ('mn_Url', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='ma_part',
            name='mn_id',
            field=models.ForeignKey(to='polls.Mn_Name', null=True),
        ),
    ]
