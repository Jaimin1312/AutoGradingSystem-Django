# Generated by Django 3.0.8 on 2020-08-16 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_student_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='student',
            field=models.ManyToManyField(to='main.Student'),
        ),
    ]
