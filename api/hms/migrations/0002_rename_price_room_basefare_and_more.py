# Generated by Django 5.0.6 on 2024-05-15 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hms', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='price',
            new_name='baseFare',
        ),
        migrations.RenameField(
            model_name='room',
            old_name='bedSize',
            new_name='roomSize',
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='max_price',
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='min_price',
        ),
        migrations.RemoveField(
            model_name='room',
            name='room_numbers',
        ),
    ]
