# Generated by Django 3.1.2 on 2020-10-07 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruit',
            name='company_name',
            field=models.CharField(max_length=45),
        ),
    ]