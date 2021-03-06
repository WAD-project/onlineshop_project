# Generated by Django 2.2.3 on 2020-03-06 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reuse', '0005_userprofile_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('products', models.ManyToManyField(to='reuse.CurrentProduct')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='reuse.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('products', models.ManyToManyField(to='reuse.CurrentProduct')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='reuse.UserProfile')),
            ],
        ),
    ]
