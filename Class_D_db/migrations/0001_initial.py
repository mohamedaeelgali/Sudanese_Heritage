# Generated by Django 3.2.14 on 2022-08-06 01:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClassToolDescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Person name')),
                ('description', models.TextField(blank=True, max_length=500)),
                ('username', models.CharField(default='admin', max_length=60)),
                ('approved', models.CharField(choices=[('y', 'Yes'), ('n', 'No')], default='y', max_length=1, verbose_name='Approved')),
                ('ip', models.CharField(default='None', max_length=50)),
                ('time', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClassZipUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=120, verbose_name='comment')),
                ('zip_file', models.FileField(upload_to='zip/')),
                ('username', models.CharField(default='admin', max_length=60)),
                ('approved', models.CharField(choices=[('y', 'Yes'), ('n', 'No')], default='y', max_length=1, verbose_name='Approved')),
                ('time', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClassToolImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='admin', max_length=60)),
                ('img', models.ImageField(upload_to='class_c/')),
                ('approved', models.CharField(choices=[('y', 'Yes'), ('n', 'No')], default='y', max_length=1, verbose_name='Approved')),
                ('time', models.DateTimeField(auto_now_add=True, null=True)),
                ('ip', models.CharField(default='None', max_length=50)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Class_D_db.classtooldescription')),
            ],
        ),
    ]
