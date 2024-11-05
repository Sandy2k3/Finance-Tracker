# Generated by Django 5.1.1 on 2024-11-04 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcategory',
            name='category',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='subcat',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='user',
        ),
        migrations.RemoveField(
            model_name='usercategory',
            name='user',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_category',
            field=models.CharField(choices=[('business', 'Business'), ('personal', 'Personal')], default='personal', max_length=10),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='SubCategory',
        ),
        migrations.DeleteModel(
            name='Transaction',
        ),
        migrations.DeleteModel(
            name='UserCategory',
        ),
    ]