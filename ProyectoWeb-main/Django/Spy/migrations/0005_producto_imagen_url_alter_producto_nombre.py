# Generated by Django 5.0.6 on 2024-10-26 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Spy', '0004_alter_producto_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='imagen_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
    ]