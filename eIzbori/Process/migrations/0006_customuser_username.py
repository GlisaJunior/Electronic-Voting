# Generated by Django 4.1.4 on 2023-06-18 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Process', '0005_alter_customuser_votestatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='username',
            field=models.CharField(default='', max_length=150),
        ),
    ]