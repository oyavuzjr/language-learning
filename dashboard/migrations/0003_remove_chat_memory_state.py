# Generated by Django 4.2.8 on 2024-06-09 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_chat_memory_state'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='memory_state',
        ),
    ]
