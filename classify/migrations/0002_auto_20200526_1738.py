# Generated by Django 3.0.6 on 2020-05-26 17:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('classify', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='detectionscore',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterUniqueTogether(
            name='detectionscore',
            unique_together={('user', 'detection', 'kind')},
        ),
    ]
