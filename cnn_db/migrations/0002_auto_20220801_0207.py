# Generated by Django 3.2.14 on 2022-07-31 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cnn_db', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='class_person_description',
            new_name='ClassPersonDescription',
        ),
        migrations.RenameModel(
            old_name='class_person_images',
            new_name='ClassPersonImages',
        ),
    ]