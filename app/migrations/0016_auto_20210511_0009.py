# Generated by Django 3.1.7 on 2021-05-11 04:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20210505_0024'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='medicion',
            options={'ordering': ('fecha_creacion',), 'verbose_name_plural': 'Mediciones'},
        ),
        migrations.RemoveField(
            model_name='pila',
            name='estado',
        ),
    ]
