from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Profile, Course, Bookmark
from .serializers import ProfileSerializer, CourseSerializer, BookmarkSerializer


@api_view(["GET"])
def health(request):
    return Response({"status": "ok"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def recommendations(request):
    # TODO: replace with real ranking logic later
    limit = int(request.query_params.get("limit", 5))
    # honor the requested limit when slicing recommendations
    courses = Course.objects.all().order_by("dept", "course_id")[:limit]
    data = CourseSerializer(courses, many=True).data
    return Response({"recommendations": data})


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return only the current user's profile"""
        return Profile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Set the user to the current user when creating a profile"""
        serializer.save(user=self.request.user)

    def get_object(self):
        """Return the current user's profile or create one if it doesn't exist"""
        try:
            return self.get_queryset().get()
        except Profile.DoesNotExist:
            # Create a profile for the user if it doesn't exist
            return Profile.objects.create(user=self.request.user)


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for courses - no create/update/delete for MVP"""

    queryset = Course.objects.all().order_by("dept", "course_id")
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]


class BookmarkViewSet(viewsets.ModelViewSet):
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return only the current user's bookmarks"""
        return Bookmark.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        """Set the user to the current user when creating a bookmark"""
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        """Add request to serializer context for user validation"""
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
