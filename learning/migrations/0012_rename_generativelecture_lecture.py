# Generated by Django 4.2.8 on 2024-06-21 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0011_rename_completionquestiontool_completionquestion_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GenerativeLecture',
            new_name='Lecture',
        ),
    ]
