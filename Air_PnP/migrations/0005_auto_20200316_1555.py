# Generated by Django 3.0.3 on 2020-03-16 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Air_PnP', '0004_auto_20200316_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bathrooms',
            name='address_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bathrooms', to='Air_PnP.Addresses'),
        ),
    ]