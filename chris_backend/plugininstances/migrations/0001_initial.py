# Generated by Django 4.2.5 on 2024-04-10 04:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import plugins.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('feeds', '0001_initial'),
        ('plugins', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workflows', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='PluginInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('created', 'Default initial'), ('waiting', 'Waiting to be scheduled'), ('scheduled', 'Scheduled on worker'), ('started', 'Started on compute env'), ('registeringFiles', 'Registering output files'), ('finishedSuccessfully', 'Finished successfully'), ('finishedWithError', 'Finished with error'), ('cancelled', 'Cancelled')], default='created', max_length=30)),
                ('summary', models.CharField(blank=True, max_length=4000)),
                ('raw', models.TextField(blank=True)),
                ('size', models.BigIntegerField(default=0)),
                ('error_code', models.CharField(blank=True, max_length=7)),
                ('cpu_limit', plugins.fields.CPUField(null=True)),
                ('memory_limit', plugins.fields.MemoryField(null=True)),
                ('number_of_workers', models.IntegerField(null=True)),
                ('gpu_limit', models.IntegerField(null=True)),
                ('compute_resource', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='plugin_instances', to='plugins.computeresource')),
                ('feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plugin_instances', to='feeds.feed')),
                ('output_folder', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='plugin_inst', to='core.chrisfolder')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('plugin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instances', to='plugins.plugin')),
                ('previous', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next', to='plugininstances.plugininstance')),
                ('workflow', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='plugin_instances', to='workflows.workflow')),
            ],
            options={
                'ordering': ('-start_date',),
            },
        ),
        migrations.CreateModel(
            name='PluginInstanceSplit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('filter', models.CharField(blank=True, max_length=600)),
                ('created_plugin_inst_ids', models.CharField(max_length=600)),
                ('plugin_inst', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='splits', to='plugininstances.plugininstance')),
            ],
            options={
                'ordering': ('plugin_inst', '-creation_date'),
            },
        ),
        migrations.CreateModel(
            name='PluginInstanceLock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plugin_inst', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='lock', to='plugininstances.plugininstance')),
            ],
        ),
        migrations.CreateModel(
            name='UnextpathParameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=16000)),
                ('plugin_inst', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unextpath_param', to='plugininstances.plugininstance')),
                ('plugin_param', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unextpath_inst', to='plugins.pluginparameter')),
            ],
            options={
                'unique_together': {('plugin_inst', 'plugin_param')},
            },
        ),
        migrations.CreateModel(
            name='StrParameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(blank=True, max_length=600)),
                ('plugin_inst', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='string_param', to='plugininstances.plugininstance')),
                ('plugin_param', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='string_inst', to='plugins.pluginparameter')),
            ],
            options={
                'unique_together': {('plugin_inst', 'plugin_param')},
            },
        ),
        migrations.CreateModel(
            name='PathParameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=16000)),
                ('plugin_inst', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='path_param', to='plugininstances.plugininstance')),
                ('plugin_param', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='path_inst', to='plugins.pluginparameter')),
            ],
            options={
                'unique_together': {('plugin_inst', 'plugin_param')},
            },
        ),
        migrations.CreateModel(
            name='IntParameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('plugin_inst', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='integer_param', to='plugininstances.plugininstance')),
                ('plugin_param', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='integer_inst', to='plugins.pluginparameter')),
            ],
            options={
                'unique_together': {('plugin_inst', 'plugin_param')},
            },
        ),
        migrations.CreateModel(
            name='FloatParameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('plugin_inst', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='float_param', to='plugininstances.plugininstance')),
                ('plugin_param', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='float_inst', to='plugins.pluginparameter')),
            ],
            options={
                'unique_together': {('plugin_inst', 'plugin_param')},
            },
        ),
        migrations.CreateModel(
            name='BoolParameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.BooleanField()),
                ('plugin_inst', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boolean_param', to='plugininstances.plugininstance')),
                ('plugin_param', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boolean_inst', to='plugins.pluginparameter')),
            ],
            options={
                'unique_together': {('plugin_inst', 'plugin_param')},
            },
        ),
    ]
