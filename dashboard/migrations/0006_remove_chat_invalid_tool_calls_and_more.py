# Generated by Django 4.2.8 on 2024-06-20 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_chat_invalid_tool_calls_chat_tool_calls'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='invalid_tool_calls',
        ),
        migrations.RemoveField(
            model_name='chat',
            name='tool_calls',
        ),
    ]