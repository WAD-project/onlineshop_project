# Generated by Django 2.2.3 on 2020-03-24 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reuse', '0010_auto_20200324_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(default='default-user.png', upload_to='profile_images'),
        ),
    ]