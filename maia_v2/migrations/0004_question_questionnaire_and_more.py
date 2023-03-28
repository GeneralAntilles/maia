# Generated by Django 4.1.7 on 2023-03-28 00:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maia_v2', '0003_questionnaire_questionnaireresponse_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='questionnaire',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='maia_v2.questionnaire'),
        ),
        migrations.AddField(
            model_name='questioncategory',
            name='questionnaire',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='maia_v2.questionnaire'),
        ),
    ]
