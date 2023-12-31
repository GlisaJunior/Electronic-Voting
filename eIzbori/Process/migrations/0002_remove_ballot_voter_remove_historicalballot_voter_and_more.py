# Generated by Django 4.2.1 on 2023-06-08 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Process', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ballot',
            name='voter',
        ),
        migrations.RemoveField(
            model_name='historicalballot',
            name='voter',
        ),
        migrations.AddField(
            model_name='customuser',
            name='votestatus',
            field=models.IntegerField(choices=[(0, 'Candidacy Phase'), (1, 'Voting Phase'), (2, 'Election Over')], default=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='election',
            name='Phase',
            field=models.IntegerField(choices=[(0, 'Candidacy Phase'), (1, 'Voting Phase'), (2, 'Election Over')]),
        ),
    ]
