# Generated by Django 4.2.7 on 2023-12-05 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_questionresponse_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionnaire',
            name='date_of_questionnaire',
            field=models.DateField(auto_now=True),
        ),
    ]
