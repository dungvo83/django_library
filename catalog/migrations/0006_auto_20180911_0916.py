# Generated by Django 2.1 on 2018-09-11 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_auto_20180907_0809'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['last_name', 'first_name'], 'permissions': (('author_all', 'set_author_all'),)},
        ),
    ]