# Generated by Django 4.0.3 on 2022-04-15 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientapp', '0008_complaint'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='cdate',
            field=models.DateField(null=True),
        ),
    ]
