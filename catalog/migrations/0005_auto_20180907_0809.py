# Generated by Django 2.1 on 2018-09-07 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20180907_0425'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'set_book_as_returned'), ('can_show_borrowed_all', 'set_show_borrowed_all'))},
        ),
    ]