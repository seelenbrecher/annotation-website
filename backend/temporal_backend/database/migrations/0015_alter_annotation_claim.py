# Generated by Django 3.2 on 2022-11-17 06:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0014_alter_annotation_claim'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annotation',
            name='claim',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='annotations', to='database.claim'),
        ),
    ]
