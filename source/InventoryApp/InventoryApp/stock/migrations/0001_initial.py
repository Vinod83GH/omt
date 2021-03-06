# Generated by Django 2.2.5 on 2019-09-05 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product_catalogue', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockOut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tax', models.DecimalField(decimal_places=2, max_digits=4)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_catalogue.Product')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_catalogue.ProductUnit')),
            ],
        ),
        migrations.CreateModel(
            name='StockIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tax', models.DecimalField(decimal_places=2, max_digits=4)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_catalogue.Product')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_catalogue.ProductUnit')),
            ],
        ),
        migrations.CreateModel(
            name='StockBalance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tax', models.DecimalField(decimal_places=2, max_digits=4)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_catalogue.Product')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_catalogue.ProductUnit')),
            ],
        ),
    ]
