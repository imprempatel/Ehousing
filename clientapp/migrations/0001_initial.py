# Generated by Django 4.0.3 on 2022-03-28 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=50)),
                ('lname', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('mobile', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=20)),
                ('society_type', models.CharField(max_length=50)),
                ('lane', models.CharField(max_length=50)),
                ('house_no', models.CharField(max_length=10)),
                ('residence_type', models.CharField(max_length=20)),
            ],
        ),
    ]
