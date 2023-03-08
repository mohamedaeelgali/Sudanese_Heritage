# Generated by Django 3.2.14 on 2022-07-31 23:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cnn_db', '0003_rename_classpersonimages_classpersonimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classpersonimage',
            name='name',
        ),
        migrations.AddField(
            model_name='classpersonimage',
            name='person_name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cnn_db.classpersondescription'),
            preserve_default=False,
        ),
    ]
