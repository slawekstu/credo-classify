# Generated by Django 3.0.4 on 2020-03-14 19:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classified',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date of classified')),
                ('detection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.Detection', verbose_name='Detection')),
            ],
            options={
                'verbose_name': 'Classified detection',
                'verbose_name_plural': 'Classified detections',
                'default_permissions': ('view', 'add', 'change', 'delete'),
            },
        ),
    ]
