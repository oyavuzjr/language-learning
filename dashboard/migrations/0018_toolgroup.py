# Generated by Django 4.2.8 on 2024-06-23 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0017_multiplechoicequestion'),
    ]

    operations = [
        migrations.CreateModel(
            name='ToolGroup',
            fields=[
                ('basemessage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.basemessage')),
                ('tool_messages', models.ManyToManyField(related_name='tool_groups', to='dashboard.toolmessage')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('dashboard.basemessage',),
        ),
    ]