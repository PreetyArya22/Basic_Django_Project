# Generated by Django 5.1.4 on 2025-01-14 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0002_question_question_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.CharField(max_length=200),
        ),
    ]
