# Generated by Django 5.1.1 on 2024-10-03 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_payment"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="payment",
            options={
                "ordering": ["-payment_date"],
                "verbose_name": "Платеж",
                "verbose_name_plural": "Платежи",
            },
        ),
        migrations.AlterField(
            model_name="payment",
            name="payment_method",
            field=models.CharField(
                choices=[("cash", "наличные"), ("transfer", "перевод на счет")],
                max_length=20,
                verbose_name="Метод оплаты",
            ),
        ),
    ]
