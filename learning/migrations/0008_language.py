# Generated by Django 4.2.8 on 2024-06-09 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0007_completionquestion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]