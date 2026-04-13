from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="display_name",
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="email",
        ),
        migrations.AddField(
            model_name="userprofile",
            name="role",
            field=models.CharField(
                choices=[("user", "User"), ("admin", "Admin")],
                default="user",
                max_length=16,
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="user",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=models.deletion.CASCADE,
                related_name="profile",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterModelTable(
            name="userprofile",
            table="users_profile",
        ),
    ]
