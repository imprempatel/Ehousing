# Generated by Django 4.0.3 on 2022-04-11 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_user_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ename', models.CharField(max_length=20)),
                ('edate', models.DateField()),
                ('evenue', models.CharField(max_length=20)),
                ('edes', models.TextField(default=True, null=True)),
                ('secretary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
            ],
        ),
    ]
