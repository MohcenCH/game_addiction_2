# Generated by Django 4.2.7 on 2024-01-05 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0040_alter_thread_unique_together_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='loginCount',
        ),
    ]
