# Generated by Django 2.2.3 on 2020-03-24 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reuse', '0012_auto_20200324_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='address',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='postcode',
            field=models.CharField(max_length=10),
        ),
    ]
