# Generated by Django 4.1.5 on 2023-01-17 22:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PoapClaim',
            new_name='DirectPoapClaim',
        ),
    ]
