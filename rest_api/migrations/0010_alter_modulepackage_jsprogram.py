# Generated by Django 3.2.9 on 2021-12-02 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0009_auto_20211202_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modulepackage',
            name='JSProgram',
            field=models.TextField(default='', max_length=10000000),
        ),
    ]
