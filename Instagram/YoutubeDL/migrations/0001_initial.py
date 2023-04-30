# Generated by Django 4.2 on 2023-04-22 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="YoutubeModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("content", models.CharField(max_length=100)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
