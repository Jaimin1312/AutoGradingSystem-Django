# Generated by Django 3.1.1 on 2020-09-24 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_auto_20200924_1841'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testcase',
            name='expectedoutput',
        ),
    ]
