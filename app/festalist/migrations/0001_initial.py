# Generated by Django 2.2.10 on 2020-03-05 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FestaList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=150)),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('host', models.CharField(blank=True, max_length=150)),
                ('date', models.CharField(blank=True, max_length=150)),
                ('content', models.CharField(blank=True, max_length=150)),
                ('apply', models.CharField(blank=True, max_length=150)),
                ('tickets', models.CharField(blank=True, max_length=150)),
                ('link', models.CharField(blank=True, max_length=150)),
            ],
        ),
    ]
