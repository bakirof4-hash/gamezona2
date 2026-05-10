from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0010_score"),
    ]

    operations = [
        migrations.CreateModel(
            name="HorrorRoom",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=8, unique=True)),
                ("name", models.CharField(max_length=120)),
                ("location", models.CharField(default="abandoned-hospital", max_length=40)),
                ("atmosphere", models.CharField(default="Something is breathing behind the walls.", max_length=220)),
                ("screamer", models.CharField(blank=True, default="", max_length=40)),
                ("screamer_text", models.CharField(blank=True, default="", max_length=220)),
                ("host_session", models.CharField(max_length=64)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="HorrorPresence",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("session_key", models.CharField(max_length=64)),
                ("nickname", models.CharField(max_length=40)),
                ("accent", models.CharField(default="#ff5c75", max_length=16)),
                ("joined_at", models.DateTimeField(auto_now_add=True)),
                ("last_seen", models.DateTimeField(auto_now=True)),
                ("room", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="players", to="main.horrorroom")),
            ],
            options={
                "unique_together": {("room", "session_key")},
            },
        ),
    ]
