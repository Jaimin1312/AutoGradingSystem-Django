# Generated by Django 3.0.8 on 2020-08-16 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_batch_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='language',
            field=models.ManyToManyField(to='main.Language'),
        ),
    ]
