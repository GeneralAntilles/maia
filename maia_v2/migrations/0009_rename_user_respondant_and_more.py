# Generated by Django 4.1.7 on 2023-04-08 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maia_v2', '0008_question_required'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='Respondant',
        ),
        migrations.RenameField(
            model_name='questionnaireresponse',
            old_name='user',
            new_name='respondant',
        ),
    ]
