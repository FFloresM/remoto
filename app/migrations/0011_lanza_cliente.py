# Generated by Django 3.1.6 on 2021-03-17 02:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20210223_0213'),
    ]

    operations = [
        migrations.AddField(
            model_name='lanza',
            name='cliente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.cliente'),
        ),
    ]
