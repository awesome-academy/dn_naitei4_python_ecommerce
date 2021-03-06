# Generated by Django 3.2.3 on 2021-06-16 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='status',
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('W', 'waiting'), ('A', 'approved'), ('R', 'rejected')], default='W', help_text='Booking state', max_length=2),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('U', 'user'), ('M', 'manager')], default='U', help_text='User role', max_length=2),
        ),
    ]
