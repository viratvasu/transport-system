# Generated by Django 3.0.8 on 2021-03-23 04:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0003_truck'),
    ]

    operations = [
        migrations.AlterField(
            model_name='truck',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trucks', to='branch.BranchProfile'),
        ),
    ]
