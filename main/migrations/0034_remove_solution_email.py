# Generated by Django 3.1.1 on 2020-09-24 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_testcase_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solution',
            name='email',
        ),
    ]
