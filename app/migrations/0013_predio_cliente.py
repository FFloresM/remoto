# Generated by Django 3.1.7 on 2021-04-13 00:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20210318_2007'),
    ]

    operations = [
        migrations.AddField(
            model_name='predio',
            name='cliente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.cliente'),
        ),
    ]
