# Generated by Django 3.0.7 on 2021-05-24 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('templatestore', '0006_template_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='templateversion',
            name='user_email',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]