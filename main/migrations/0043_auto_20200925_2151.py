# Generated by Django 3.1.1 on 2020-09-25 21:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0042_auto_20200925_2135'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testcaseoutput',
            old_name='studentoutput',
            new_name='studentcodeoutput',
        ),
    ]
