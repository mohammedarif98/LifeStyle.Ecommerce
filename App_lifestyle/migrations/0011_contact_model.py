# Generated by Django 4.1.2 on 2022-10-31 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_lifestyle', '0010_mens_product_model_size_women_product_model_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact_Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100, null=True)),
                ('Message', models.TextField(max_length=1000)),
                ('Email', models.EmailField(max_length=100)),
            ],
        ),
    ]
