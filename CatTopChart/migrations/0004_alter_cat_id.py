# Generated by Django 4.2.4 on 2023-09-11 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CatTopChart', '0003_alter_cat_rank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cat',
            name='id',
            field=models.CharField(help_text='Cat image id. example: eOLpJytrbsQ', max_length=200, primary_key=True, serialize=False),
        ),
    ]