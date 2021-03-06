# Generated by Django 3.1.5 on 2021-02-06 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='left',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='right',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='tree_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
