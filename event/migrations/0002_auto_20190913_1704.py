# Generated by Django 2.2.5 on 2019-09-13 17:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='players',
            field=models.PositiveSmallIntegerField(default=4, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)]),
        ),
        migrations.AlterField(
            model_name='event',
            name='point_at_start',
            field=models.PositiveSmallIntegerField(default=25000, validators=[django.core.validators.MinValueValidator(20000), django.core.validators.MaxValueValidator(30000)]),
        ),
        migrations.AlterField(
            model_name='event',
            name='rounding_method',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Floor'), (2, 'Ceil'), (3, '4/5'), (4, '5/6')], default=4),
        ),
        migrations.AlterField(
            model_name='event',
            name='uma_method',
            field=models.CharField(choices=[('A1', 'A1'), ('A2', 'A2'), ('A3', 'A3'), ('B1', 'B1'), ('B2', 'B2'), ('B3', 'B3')], default='B1', max_length=2),
        ),
        migrations.AlterField(
            model_name='result',
            name='point',
            field=models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(-200000), django.core.validators.MaxValueValidator(200000)]),
        ),
        migrations.AlterField(
            model_name='result',
            name='pt',
            field=models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(-200), django.core.validators.MaxValueValidator(200)]),
        ),
        migrations.AlterField(
            model_name='result',
            name='rank',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)]),
        ),
    ]
