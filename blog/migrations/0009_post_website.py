# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20150621_2048'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='website',
            field=models.CharField(max_length=2000, blank=True),
        ),
    ]
