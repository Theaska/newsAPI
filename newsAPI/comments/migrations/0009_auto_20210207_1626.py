# Generated by Django 3.1.5 on 2021-02-07 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0008_auto_20210207_1601'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='depth',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='rgt',
        ),
        migrations.AddField(
            model_name='comment',
            name='level',
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='rght',
            field=models.PositiveIntegerField(default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='lft',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='tree_id',
            field=models.PositiveIntegerField(db_index=True, editable=False),
        ),
    ]