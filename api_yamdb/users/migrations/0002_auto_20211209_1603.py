# Generated by Django 2.2.16 on 2021-12-09 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Код подтверждения'),
        ),
    ]
