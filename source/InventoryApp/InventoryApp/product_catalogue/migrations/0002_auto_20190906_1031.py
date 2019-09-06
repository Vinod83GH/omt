# Generated by Django 2.2.5 on 2019-09-06 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_catalogue', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='id',
            field=models.AutoField(auto_created=True, default='1', primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
