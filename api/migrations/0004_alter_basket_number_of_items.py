# Generated by Django 4.1.4 on 2023-01-09 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_category_options_alter_cashback_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='number_of_items',
            field=models.PositiveIntegerField(default=None, null=True),
        ),
    ]