# Generated by Django 5.0.2 on 2024-02-28 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puzzles', '0006_rename_solves_solve'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solve',
            name='solved',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
