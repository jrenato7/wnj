# Generated by Django 2.0.5 on 2018-07-13 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galleries', '0003_auto_20180712_0219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]
