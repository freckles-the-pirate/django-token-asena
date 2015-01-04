# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=200)),
                ('comment', models.TextField(max_length=1000, null=True, blank=True)),
                ('disabled', models.BooleanField(default=False)),
                ('expiration', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Token',
                'verbose_name_plural': 'Tokens',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TokenSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('generated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200, null=True, blank=True)),
                ('disabled', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Token Set',
                'verbose_name_plural': 'Token Sets',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='token',
            name='token_set',
            field=models.ForeignKey(related_query_name=b'tokens', related_name='tokens', to='asena.TokenSet'),
            preserve_default=True,
        ),
    ]
