# Generated by Django 4.2.8 on 2024-06-08 22:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('learning', '0004_rename_answer_question_correct_answer_question_title_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='freeresponsequestion',
            name='title',
        ),
        migrations.RemoveField(
            model_name='freeresponsequestion',
            name='user_answer',
        ),
        migrations.RemoveField(
            model_name='multiplechoicequestion',
            name='title',
        ),
        migrations.RemoveField(
            model_name='multiplechoicequestion',
            name='user_answer',
        ),
        migrations.RemoveField(
            model_name='question',
            name='title',
        ),
        migrations.RemoveField(
            model_name='question',
            name='user_answer',
        ),
        migrations.AddField(
            model_name='freeresponsequestion',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='multiplechoicequestion',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='freeresponsequestion',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='multiplechoicequestion',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='question',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('correct', models.BooleanField()),
                ('user_answer', models.TextField()),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]