# Generated by Django 2.1.7 on 2019-03-17 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('siem', '0026_auto_20190317_1713'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='limitrule',
            unique_together={('name', 'is_builtin')},
        ),
    ]