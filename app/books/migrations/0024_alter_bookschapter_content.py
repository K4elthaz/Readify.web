# Generated by Django 5.1.1 on 2024-11-28 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0023_proofofpaymentbyuser_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bookschapter",
            name="content",
            field=models.TextField(unique=True),
        ),
    ]
