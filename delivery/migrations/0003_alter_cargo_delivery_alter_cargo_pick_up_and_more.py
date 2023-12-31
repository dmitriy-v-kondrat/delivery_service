# Generated by Django 4.2.4 on 2023-09-11 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0002_rename_car_truck'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cargo',
            name='delivery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delivery', to='delivery.location', to_field='zip_code'),
        ),
        migrations.AlterField(
            model_name='cargo',
            name='pick_up',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pick_up', to='delivery.location', to_field='zip_code'),
        ),
        migrations.AlterField(
            model_name='truck',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='delivery.location', to_field='zip_code'),
        ),
    ]
