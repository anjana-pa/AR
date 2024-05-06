# Generated by Django 3.2.25 on 2024-04-07 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Furniture_shopping', '0002_auto_20240328_1347'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(max_length=1000)),
                ('rating', models.CharField(max_length=1000)),
                ('PRODUCT', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Furniture_shopping.product')),
                ('USER', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Furniture_shopping.user')),
            ],
        ),
    ]