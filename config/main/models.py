from django.contrib.auth.models import User
from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Grade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    value = models.IntegerField()
    date = models.DateField(auto_now_add=True)


class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="items/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_name = models.CharField(max_length=100)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.score}"


class HorrorRoom(models.Model):
    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=40, default="abandoned-hospital")
    atmosphere = models.CharField(max_length=220, default="Something is breathing behind the walls.")
    screamer = models.CharField(max_length=40, blank=True, default="")
    screamer_text = models.CharField(max_length=220, blank=True, default="")
    host_session = models.CharField(max_length=64)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class HorrorPresence(models.Model):
    room = models.ForeignKey(HorrorRoom, on_delete=models.CASCADE, related_name="players")
    session_key = models.CharField(max_length=64)
    nickname = models.CharField(max_length=40)
    accent = models.CharField(max_length=16, default="#ff5c75")
    joined_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("room", "session_key")

    def __str__(self):
        return f"{self.nickname} @ {self.room.code}"


class Visitor(models.Model):
    session_key = models.CharField(max_length=64, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    display_name = models.CharField(max_length=150)
    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name
