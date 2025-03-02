# Generated by Django 5.1.1 on 2024-12-11 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0006_customuser_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
