# Generated by Django 2.2.3 on 2020-03-06 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reuse', '0004_remove_userprofile_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='slug',
            field=models.SlugField(default='', unique=True),
            preserve_default=False,
        ),
    ]
