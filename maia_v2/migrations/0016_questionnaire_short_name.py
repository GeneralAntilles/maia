# Generated by Django 4.1.7 on 2023-04-12 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maia_v2', '0015_questionnaire_scale_questionnaire_scale_max_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaire',
            name='short_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]