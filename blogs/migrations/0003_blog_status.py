# Generated by Django 4.1.3 on 2022-12-12 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_remove_user_name_alter_user_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='status',
            field=models.CharField(choices=[('pending', 'Kutilmoqda'), ('active', 'Faol'), ('cancel', 'Rad etilgan')], default='pending', max_length=25),
        ),
    ]