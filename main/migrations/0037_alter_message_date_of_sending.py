# Generated by Django 4.2.7 on 2024-01-04 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='date_of_sending',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]