# Generated by Django 4.2 on 2023-05-18 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='text_preview',
            field=models.CharField(blank=True, max_length=90, null=True),
        ),
    ]