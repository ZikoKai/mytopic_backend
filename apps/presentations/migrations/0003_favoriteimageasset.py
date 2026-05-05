from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("presentations", "0002_presentationdocument"),
    ]

    operations = [
        migrations.CreateModel(
            name="FavoriteImageAsset",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(blank=True, default="", max_length=255)),
                ("prompt", models.CharField(blank=True, default="", max_length=1200)),
                ("image_data_url", models.TextField()),
                (
                    "mime_type",
                    models.CharField(blank=True, default="image/png", max_length=64),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="favorite_image_assets",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "favorite_image_assets",
                "ordering": ["-updated_at"],
            },
        ),
    ]
