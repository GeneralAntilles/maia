# Generated by Django 4.2.7 on 2023-11-28 03:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("maia_v2", "0020_questionnaireresponse_score"),
    ]

    operations = [
        migrations.AddField(
            model_name="questionnaire",
            name="preview_image",
            field=models.ImageField(
                blank=True, null=True, upload_to="questionnaire_images"
            ),
        ),
    ]
