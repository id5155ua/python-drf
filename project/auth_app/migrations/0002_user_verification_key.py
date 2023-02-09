# Generated by Django 3.2 on 2023-02-09 16:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='verification_key',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
