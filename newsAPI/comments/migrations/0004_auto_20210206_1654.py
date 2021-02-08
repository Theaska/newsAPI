# Generated by Django 3.1.5 on 2021-02-06 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_auto_20210206_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='left',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='comment',
            name='level',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='comment',
            name='right',
            field=models.PositiveIntegerField(default=2),
        ),
    ]
