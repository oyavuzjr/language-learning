# Generated by Django 4.2.8 on 2024-06-21 14:28

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_message_remove_humanmessage_chat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='tools_data',
            field=jsonfield.fields.JSONField(default=dict),
        ),
    ]
