# Generated by Django 5.1.2 on 2024-11-29 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('motion', '0003_alter_fitnessclass_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainer',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
