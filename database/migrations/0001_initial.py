# Generated by Django 3.0.3 on 2020-02-23 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CredoUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('display_name', models.CharField(max_length=50)),
            ],
            options={
                'default_permissions': ('view', 'add', 'change', 'delete'),
            },
        ),
        migrations.CreateModel(
            name='Detection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.BigIntegerField(db_index=True)),
                ('time_received', models.BigIntegerField(blank=True)),
                ('mime', models.CharField(default='image/png', max_length=32)),
                ('source', models.CharField(blank=True, max_length=255)),
                ('provider', models.CharField(blank=True, max_length=255)),
                ('metadata', models.TextField(blank=True, null=True)),
            ],
            options={
                'default_permissions': ('view', 'add', 'change', 'delete'),
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(max_length=255)),
                ('device_type', models.CharField(default='phone_android', max_length=255)),
                ('device_model', models.CharField(max_length=255)),
                ('system_version', models.CharField(max_length=255)),
            ],
            options={
                'default_permissions': ('view', 'add', 'change', 'delete'),
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, unique=True)),
            ],
            options={
                'default_permissions': ('view', 'add', 'change', 'delete'),
            },
        ),
        migrations.CreateModel(
            name='Ping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.BigIntegerField(db_index=True)),
                ('time_received', models.BigIntegerField(blank=True)),
                ('delta_time', models.IntegerField(blank=True, null=True)),
                ('on_time', models.IntegerField(blank=True, default=0, null=True)),
                ('metadata', models.TextField(blank=True, null=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Device')),
            ],
        ),
    ]
