"""Generated by Django 3.1.1 on 2020-09-14 22:15."""

import django.db.models.deletion

from django.db import migrations, models


class Migration(migrations.Migration):
    """Keep track of failed imports."""

    dependencies = [
        ("codex", "0003_auto_20200831_2033"),
    ]

    operations = [
        migrations.CreateModel(
            name="FailedImport",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("path", models.CharField(db_index=True, max_length=128)),
                ("reason", models.CharField(max_length=64)),
                (
                    "library",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="codex.library"
                    ),
                ),
            ],
            options={
                "unique_together": {("library", "path")},
            },
        ),
    ]
