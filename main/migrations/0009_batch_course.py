# Generated by Django 3.0.8 on 2020-08-16 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_batch_instructor'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='course',
            field=models.ManyToManyField(to='main.Course'),
        ),
    ]