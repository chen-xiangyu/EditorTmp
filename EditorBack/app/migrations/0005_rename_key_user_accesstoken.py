# Generated by Django 5.0.6 on 2024-07-10 09:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_user_password'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='key',
            new_name='accessToken',
        ),
    ]
