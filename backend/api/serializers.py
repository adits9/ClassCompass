from rest_framework import serializers
from .models import Profile, Course, Bookmark


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "user", "major", "year"]
        read_only_fields = ["id", "user"]

    def create(self, validated_data):
        """Ensure user is set to the current user"""
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "course_id", "dept", "title", "credits"]


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ["id", "user", "course", "created_at"]
        read_only_fields = ["id", "user", "created_at"]

    def create(self, validated_data):
        """Ensure user is set to the current user and handle duplicates"""
        validated_data["user"] = self.context["request"].user
        try:
            return super().create(validated_data)
        except Exception as e:
            # Handle duplicate bookmark creation gracefully
            if "unique constraint" in str(e).lower():
                raise serializers.ValidationError("This course is already bookmarked.")
            raise e
