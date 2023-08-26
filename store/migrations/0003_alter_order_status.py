# Generated by Django 4.1.4 on 2023-08-25 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Out For Shipping', 'Out For Shipping'), ('Completed', 'Completed'), ('Pending', 'Pending')], default='Pending', max_length=150),
        ),
    ]