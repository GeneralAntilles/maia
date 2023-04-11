# Generated by Django 4.1.7 on 2023-04-11 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maia_v2', '0014_rename_respondant_respondent_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaire',
            name='scale',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='scale_max',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='scale_min',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
