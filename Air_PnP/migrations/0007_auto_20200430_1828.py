# Generated by Django 3.0.4 on 2020-04-30 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Air_PnP', '0006_scheduler_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='bathrooms',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='bathrooms',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='bathrooms',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='bathrooms',
            name='image4',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]