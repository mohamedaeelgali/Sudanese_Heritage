# Generated by Django 3.2.14 on 2022-08-02 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnn_db', '0012_auto_20220802_0527'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassBulkUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=120, verbose_name='comment')),
                ('zip_file', models.FileField(upload_to='zip/')),
                ('username', models.CharField(default='admin', max_length=60)),
                ('approved', models.CharField(choices=[('y', 'Yes'), ('n', 'No')], default='y', max_length=1, verbose_name='Approved')),
                ('time', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
