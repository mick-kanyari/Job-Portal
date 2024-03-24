# Generated by Django 4.2.11 on 2024-03-22 08:30

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('description', ckeditor.fields.RichTextField()),
                ('location', models.CharField(max_length=300)),
                ('job_type', models.CharField(choices=[('1', 'Full OnBoard'), ('2', 'Partly Onboard'), ('3', 'Pending')], max_length=1)),
                ('capacity', models.CharField(blank=True, max_length=30)),
                ('company_name', models.CharField(max_length=300)),
                ('company_description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('url', models.URLField()),
                ('last_date', models.DateField()),
                ('is_published', models.BooleanField(default=False)),
                ('is_unavailabled', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MachineUser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vtype',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='machinery1.machine')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='machine',
            name='vtype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='VType', to='machinery1.vtype'),
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='machinery1.machine')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ClientUser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BookmarkMachine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='machinery1.machine')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
