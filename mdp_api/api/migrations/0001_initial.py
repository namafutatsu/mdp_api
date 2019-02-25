# Generated by Django 2.1.7 on 2019-02-25 22:47

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import places.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.TextField()),
                ('highlights', models.TextField(blank=True, null=True)),
                ('location', places.fields.PlacesField(max_length=255)),
                ('webpage', models.URLField(blank=True, max_length=512, null=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='')),
            ],
            options={
                'ordering': ['slug'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ShopComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField()),
                ('ranking', models.IntegerField(default=5, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mdp_api_api.Shop')),
            ],
            options={
                'ordering': ['slug'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ShopContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('kind', models.CharField(choices=[('producer', 'Producer'), ('shop', 'Shop')], default='shop', max_length=32)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
            ],
            options={
                'ordering': ['slug'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ShopNetwork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['slug'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='shop',
            name='network',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mdp_api_api.ShopNetwork'),
        ),
        migrations.AddField(
            model_name='shop',
            name='shop_contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mdp_api_api.ShopContact'),
        ),
    ]