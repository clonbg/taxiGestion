# Generated by Django 4.0.6 on 2022-07-26 21:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('licencias', '0001_initial'),
        ('taxistas', '0002_remove_user_licencia_id_user_licencia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='licencia',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='licencias.licencia'),
        ),
    ]
