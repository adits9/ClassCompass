from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    major = models.CharField(max_length=120, blank=True)
    year = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"


class Course(models.Model):
    course_id = models.CharField(max_length=50, unique=True)  # e.g., "CS 225"
    dept = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    credits = models.IntegerField(default=3)

    def __str__(self):
        return f"{self.course_id} - {self.title}"


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="bookmarks"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "course")
