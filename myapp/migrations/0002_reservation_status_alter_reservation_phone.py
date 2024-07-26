# Generated by Django 5.0.4 on 2024-07-25 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('pending', 'En attente'), ('confirmed', 'Confirmé'), ('cancelled', 'Annulé')], default='pending', max_length=10),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='phone',
            field=models.CharField(max_length=15),
        ),
    ]
