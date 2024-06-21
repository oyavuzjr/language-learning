# Generated by Django 4.2.8 on 2024-06-21 21:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_basemessage_aimessage_humanmessage_toolmessage_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompletionQuestion',
            fields=[
                ('toolmessage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dashboard.toolmessage')),
                ('correct_answer', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('dashboard.toolmessage',),
        ),
        migrations.AlterField(
            model_name='toolmessage',
            name='tool_name',
            field=models.CharField(editable=False, max_length=100),
        ),
    ]
