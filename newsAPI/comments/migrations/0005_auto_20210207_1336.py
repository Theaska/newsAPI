# Generated by Django 3.1.5 on 2021-02-07 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0004_auto_20210206_1654'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='text',
        ),
    ]