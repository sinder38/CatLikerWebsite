# Generated by Django 4.2.4 on 2023-09-11 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CatTopChart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cat',
            name='rank',
            field=models.PositiveIntegerField(blank=True, help_text='current rank of the cat compared to others'),
        ),
    ]