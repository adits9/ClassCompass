from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    health,
    recommendations,
    ProfileViewSet,
    CourseViewSet,
    BookmarkViewSet,
)

router = DefaultRouter()
router.register(r"profiles", ProfileViewSet, basename="profiles")
router.register(r"courses", CourseViewSet, basename="courses")
router.register(r"bookmarks", BookmarkViewSet, basename="bookmarks")

urlpatterns = [
    path("health/", health),
    path("recommendations/", recommendations),
    path("", include(router.urls)),
]
