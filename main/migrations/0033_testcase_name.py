# Generated by Django 3.1.1 on 2020-09-24 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_remove_testcase_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='testcase',
            name='name',
            field=models.CharField(default=0, max_length=254),
            preserve_default=False,
        ),
    ]
