# Generated by Django 4.2.3 on 2023-07-28 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imgeditor', '0002_imagefile_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagefile',
            name='processed_img',
            field=models.ImageField(blank=True, null=True, upload_to='processed/'),
        ),
    ]
