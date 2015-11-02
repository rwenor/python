# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ma_Part',
            fields=[
                ('ma_id', models.IntegerField(serialize=False, primary_key=True)),
                ('mn_nr', models.CharField(max_length=40)),
                ('mn_desc', models.CharField(max_length=40)),
                ('ma_desc', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('part_desc', models.CharField(max_length=60)),
                ('ma_id', models.ForeignKey(to='polls.Ma_Part')),
            ],
        ),
        migrations.CreateModel(
            name='Thing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('thing_desc', models.CharField(max_length=60)),
                ('ma_id', models.ForeignKey(to='polls.Ma_Part')),
            ],
        ),
    ]
