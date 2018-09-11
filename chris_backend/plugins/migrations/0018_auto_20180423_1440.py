# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-04-23 18:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import plugins.fields


class Migration(migrations.Migration):

    dependencies = [
        ('plugins', '0017_auto_20180125_1425'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComputeResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compute_resource_identifier', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='plugin',
            name='max_cpu_limit',
            field=plugins.fields.CPUField(default=2147483647, null=True),
        ),
        migrations.AddField(
            model_name='plugin',
            name='max_gpu_limit',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='plugin',
            name='max_memory_limit',
            field=plugins.fields.MemoryField(default=2147483647, null=True),
        ),
        migrations.AddField(
            model_name='plugin',
            name='max_number_of_workers',
            field=models.IntegerField(default=2147483647, null=True),
        ),
        migrations.AddField(
            model_name='plugin',
            name='min_cpu_limit',
            field=plugins.fields.CPUField(default=1000, null=True),
        ),
        migrations.AddField(
            model_name='plugin',
            name='min_gpu_limit',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='plugin',
            name='min_memory_limit',
            field=plugins.fields.MemoryField(default=200, null=True),
        ),
        migrations.AddField(
            model_name='plugin',
            name='min_number_of_workers',
            field=models.IntegerField(default=1, null=True),
        ),
        migrations.AddField(
            model_name='plugininstance',
            name='cpu_limit',
            field=plugins.fields.CPUField(null=True),
        ),
        migrations.AddField(
            model_name='plugininstance',
            name='gpu_limit',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='plugininstance',
            name='memory_limit',
            field=plugins.fields.MemoryField(null=True),
        ),
        migrations.AddField(
            model_name='plugininstance',
            name='number_of_workers',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='plugin',
            name='compute_resource',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='plugins', to='plugins.ComputeResource'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plugininstance',
            name='compute_resource',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='plugin_instances', to='plugins.ComputeResource'),
            preserve_default=False,
        ),
    ]