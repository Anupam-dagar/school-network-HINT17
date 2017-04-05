# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-25 04:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, max_length=200, null=True)),
                ('about', models.TextField(blank=True, max_length=250, null=True)),
                ('branch', models.CharField(blank=True, max_length=150, null=True)),
                ('college_name', models.CharField(blank=True, max_length=150, null=True)),
                ('established', models.DateField(blank=True, null=True)),
                ('is_product', models.BooleanField(default=False)),
                ('is_student', models.BooleanField(default=False)),
                ('is_teacher', models.BooleanField(default=False)),
                ('company', models.CharField(blank=True, max_length=100, null=True)),
                ('facebook', models.CharField(blank=True, max_length=150, null=True)),
                ('quora', models.CharField(blank=True, max_length=150, null=True)),
                ('twitter', models.CharField(blank=True, max_length=150, null=True)),
                ('linkedin', models.CharField(blank=True, max_length=150, null=True)),
                ('likes', models.IntegerField(default=1)),
                ('home', models.CharField(blank=True, max_length=100, null=True)),
                ('website', models.CharField(blank=True, max_length=100, null=True)),
                ('job', models.CharField(blank=True, max_length=100, null=True, verbose_name='what are you doing now?')),
                ('institute', models.CharField(blank=True, max_length=100, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=10, null=True)),
                ('want_to_do', models.CharField(blank=True, max_length=100, null=True, verbose_name='what do you want to do?')),
                ('likes_most', models.CharField(blank=True, max_length=100, null=True, verbose_name='who do you like most?')),
                ('likes_not', models.CharField(blank=True, max_length=100, null=True, verbose_name='who do you like not at all?')),
                ('semester', models.CharField(blank=True, max_length=10, null=True)),
                ('year', models.IntegerField(default=1)),
                ('enrolled', models.DateField(blank=True, null=True)),
                ('completed', models.DateField(blank=True, null=True)),
                ('skills', models.CharField(blank=True, max_length=200, null=True)),
                ('image', models.ImageField(blank=True, height_field='height_field', null=True, upload_to='profile_pictures', width_field='width_field')),
                ('height_field', models.IntegerField(default=450)),
                ('width_field', models.IntegerField(default=350)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'auth_profile',
            },
        ),
    ]