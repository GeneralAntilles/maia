# Generated by Django 4.1.7 on 2023-04-08 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maia_v2', '0010_alter_respondant_fingerprint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='respondant',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
