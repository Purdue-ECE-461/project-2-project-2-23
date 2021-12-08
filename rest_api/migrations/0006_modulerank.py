# Generated by Django 3.2.9 on 2021-12-08 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0005_auto_20211208_1019'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModuleRank',
            fields=[
                ('module_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('net_score', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=4)),
                ('ramp_up_score', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=4)),
                ('correctness_score', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=4)),
                ('bus_factor_score', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=4)),
                ('responsiveness_score', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=4)),
                ('dependency_score', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=4)),
                ('license_score', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=4)),
            ],
        ),
    ]