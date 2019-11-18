# Generated by Django 2.2.5 on 2019-09-17 02:07

import django.core.validators
from django.db import migrations, models
import event.models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_auto_20190913_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='players',
            field=models.PositiveSmallIntegerField(choices=[(3, '三人麻雀'), (4, '四人麻雀')], default=4),
        ),
        migrations.AlterField(
            model_name='event',
            name='point_at_start',
            field=models.PositiveIntegerField(default=25000, validators=[django.core.validators.MinValueValidator(20000), django.core.validators.MaxValueValidator(30000), event.models.validate_int_unit_1000], verbose_name='配給原点'),
        ),
        migrations.AlterField(
            model_name='event',
            name='rounding_method',
            field=models.PositiveSmallIntegerField(choices=[(1, '切落し(浮き切捨て、沈み切上げ)'), (2, '四捨五入'), (3, '五捨六入')], default=4, verbose_name='端数処理'),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(blank=True, help_text='※入力任意', max_length=50, null=True, verbose_name='イベント名'),
        ),
        migrations.AlterField(
            model_name='event',
            name='uma_method',
            field=models.CharField(choices=[('A1', '5-10'), ('A2', '10-20'), ('A3', '10-30'), ('B1', 'マルA式')], default='B1', max_length=2, verbose_name='ウマ計算方法'),
        ),
        migrations.AlterField(
            model_name='result',
            name='point',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(-200000), django.core.validators.MaxValueValidator(200000), event.models.validate_int_unit_100]),
        ),
    ]