# Generated by Django 3.1.6 on 2021-03-18 23:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_lanza_cliente'),
    ]

    operations = [
        migrations.CreateModel(
            name='Predio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='pila',
            name='predio',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.predio'),
        ),
    ]
