# Generated by Django 4.2.7 on 2023-12-24 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_feedback_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='latest_activity',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]