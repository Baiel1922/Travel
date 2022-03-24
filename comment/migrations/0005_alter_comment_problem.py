# Generated by Django 3.2.7 on 2022-03-19 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
        ('comment', '0004_alter_comment_problem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='problem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='post.post'),
        ),
    ]