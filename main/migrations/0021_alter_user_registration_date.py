# Generated by Django 4.2.7 on 2023-12-24 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='registration_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
