# Generated by Django 2.2.3 on 2020-03-28 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reuse', '0017_auto_20200328_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='on_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(choices=[(1, 'Poor'), (2, 'Average'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')], default=3),
        ),
    ]