# Generated by Django 3.2.3 on 2021-06-17 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20210527_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart1',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Total_price'),
        ),
    ]