# Generated by Django 4.0.6 on 2023-02-27 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flatmodel',
            name='features',
            field=models.ManyToManyField(help_text='You can select more than one by hold the Ctrl key', to='houses.amenitiesmodels'),
        ),
        migrations.AlterField(
            model_name='housemodel',
            name='building_type',
            field=models.CharField(choices=[('Bungalow', 'Bungalow'), ('Duplex', 'Duplex'), ('1 Story Building Apartment', '1 Story Building Apartment'), ('2 Story Building Apartment', '2 Story Building Apartment'), ('3 Story Building Apartment', '3 Story Building Apartment'), ('2 Story Building Apartment', '4 Story Building Apartment'), ('5 Story Building Apartment', '5 Story Building Apartment'), ('6 Story Building Apartment', '6 Story Building Apartment'), ('2 Story Building Plaza', '2 Story Building Plaza'), ('3 Story Building Plaza', '3 Story Building Plaza'), ('4 Story Building Plaza', '4 Story Building Plaza'), ('5 Story Building Plaza', '5 Story Building Plaza'), ('6 Story Building Plaza', '6 Story Building Plaza')], max_length=50, verbose_name='Building Type'),
        ),
        migrations.AlterField(
            model_name='housemodel',
            name='exterior_image_side1',
            field=models.ImageField(blank=True, null=True, upload_to='BuildingExterior/', verbose_name='Exterior Image Side A'),
        ),
        migrations.AlterField(
            model_name='housemodel',
            name='exterior_image_side2',
            field=models.ImageField(blank=True, null=True, upload_to='BuildingExterior/', verbose_name='Exterior Image Side B'),
        ),
        migrations.AlterField(
            model_name='housemodel',
            name='features',
            field=models.ManyToManyField(help_text='You can select more than one by hold the Ctrl key', to='houses.amenitiesmodels'),
        ),
        migrations.AlterField(
            model_name='spacemodel',
            name='features',
            field=models.ManyToManyField(help_text='You can select more than one by hold the Ctrl key', to='houses.amenitiesmodels'),
        ),
    ]