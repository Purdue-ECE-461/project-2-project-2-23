# Generated by Django 3.2.9 on 2021-12-12 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modulepackage',
            name='JSProgram',
            field=models.TextField(blank=True, default='', max_length=1000000),
        ),
    ]
