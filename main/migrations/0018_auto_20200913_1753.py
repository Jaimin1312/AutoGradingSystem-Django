# Generated by Django 3.1 on 2020-09-13 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20200913_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='batch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.batch'),
        ),
    ]