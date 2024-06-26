# Generated by Django 4.2.8 on 2024-06-21 14:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0008_aimessage_humanmessage_toolmessage_delete_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('json_data', jsonfield.fields.JSONField(default=dict)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='dashboard.chat')),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='humanmessage',
            name='chat',
        ),
        migrations.RemoveField(
            model_name='humanmessage',
            name='sender',
        ),
        migrations.RemoveField(
            model_name='toolmessage',
            name='chat',
        ),
        migrations.DeleteModel(
            name='AIMessage',
        ),
        migrations.DeleteModel(
            name='HumanMessage',
        ),
        migrations.DeleteModel(
            name='ToolMessage',
        ),
    ]
