# Generated by Django 2.0.1 on 2018-02-22 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siem', '0006_auto_20180221_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='limitrule',
            name='name',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]