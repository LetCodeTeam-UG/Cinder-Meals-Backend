# Generated by Django 4.0.7 on 2023-03-29 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_order_courier_alter_order_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='description',
            field=models.CharField(max_length=600),
        ),
    ]
