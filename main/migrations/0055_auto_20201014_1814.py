# Generated by Django 3.1.1 on 2020-10-14 18:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0054_assignment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]