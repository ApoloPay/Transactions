# Generated by Django 4.2 on 2023-06-14 03:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='parent_transaction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='backend.transaction'),
        ),
    ]