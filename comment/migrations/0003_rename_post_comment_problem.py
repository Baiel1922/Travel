# Generated by Django 3.2.7 on 2022-03-19 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_rename_problem_comment_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post',
            new_name='problem',
        ),
    ]
