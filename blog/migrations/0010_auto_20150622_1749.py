# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_post_website'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='website',
            new_name='source',
        ),
    ]
