# Generated by Django 4.2.7 on 2024-01-02 09:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_alter_user_account_type_alter_user_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alert',
            name='patient',
        ),
        migrations.AddField(
            model_name='alert',
            name='fromUser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fromUserAlerts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='alert',
            name='toUser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='toUserAlerts', to=settings.AUTH_USER_MODEL),
        ),
    ]
