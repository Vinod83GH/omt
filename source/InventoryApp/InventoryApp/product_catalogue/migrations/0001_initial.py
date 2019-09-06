# Generated by Django 2.2.5 on 2019-09-05 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('desc', models.CharField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('desc', models.CharField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductSubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('desc', models.CharField(max_length=500, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_catalogue.ProductCategory')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('code', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('desc', models.CharField(max_length=1000)),
                ('brand', models.CharField(max_length=1000, null=True)),
                ('default_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('minimum_balance', models.IntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_catalogue.ProductCategory')),
                ('default_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_catalogue.ProductUnit')),
            ],
        ),
    ]
