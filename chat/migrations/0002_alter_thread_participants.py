# Generated by Django 4.2 on 2023-04-06 17:19

from django.conf import settings
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("chat", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="thread",
            name="participants",
            field=models.ManyToManyField(
                related_name="threads",
                to=settings.AUTH_USER_MODEL,
                validators=[django.core.validators.MinLengthValidator(2)],
            ),
        ),
    ]
