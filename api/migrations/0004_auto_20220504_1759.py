# Generated by Django 3.0 on 2022-05-04 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20220504_1758'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location',
            old_name='user',
            new_name='user_foreign_key',
        ),
    ]