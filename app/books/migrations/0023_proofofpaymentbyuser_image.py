# Generated by Django 5.1.1 on 2024-11-28 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0022_remove_proofofpaymentbyuser_image_alter_books_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="proofofpaymentbyuser",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="proof_of_payment_images/"
            ),
        ),
    ]
