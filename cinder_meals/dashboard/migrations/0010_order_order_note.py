# Generated by Django 4.1.6 on 2023-03-14 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_alter_order_sub_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_note',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
