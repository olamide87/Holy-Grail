# Generated by Django 3.1.7 on 2021-03-16 02:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('holygrailapi', '0004_auto_20210315_1709'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClosetProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('closet_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='holygrailapi.closet')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='holygrailapi.product')),
            ],
        ),
    ]
