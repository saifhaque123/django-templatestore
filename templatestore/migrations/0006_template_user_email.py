# Generated by Django 3.0.7 on 2021-05-24 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('templatestore', '0005_auto_20200730_0045'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='user_email',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]