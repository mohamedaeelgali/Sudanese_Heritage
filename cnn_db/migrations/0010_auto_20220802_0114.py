# Generated by Django 3.2.14 on 2022-08-01 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnn_db', '0009_auto_20220802_0108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classpersondescription',
            name='time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='classpersonimage',
            name='time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
