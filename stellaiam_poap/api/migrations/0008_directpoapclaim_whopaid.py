# Generated by Django 4.1.5 on 2023-01-21 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_rename_idpaid_directpoapclaim_ispaid'),
    ]

    operations = [
        migrations.AddField(
            model_name='directpoapclaim',
            name='whoPaid',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
