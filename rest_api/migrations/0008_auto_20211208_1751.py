# Generated by Django 3.2.9 on 2021-12-08 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0007_auto_20211208_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='modulerank',
            name='id',
            field=models.BigAutoField(auto_created=True, default=112, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='modulerank',
            name='module_id',
            field=models.CharField(default='', max_length=255),
        ),
    ]