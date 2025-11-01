import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status
from .models import Profile, Course, Bookmark

User = get_user_model()


@pytest.mark.django_db
def test_health_ok():
    client = APIClient()
    resp = client.get("/api/health/")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


@pytest.mark.django_db
def test_unauthenticated_profile_access():
    """Test that unauthenticated users get 403"""
    client = APIClient()
    resp = client.get("/api/profiles/")
    assert resp.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_authenticated_user_can_create_profile():
    """Test that authenticated user can create their profile"""
    user = User.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    client = APIClient()
    client.force_authenticate(user=user)

    data = {"major": "Computer Science", "year": "Junior"}
    resp = client.post("/api/profiles/", data)
    assert resp.status_code == status.HTTP_201_CREATED
    assert resp.json()["user"] == user.id
    assert resp.json()["major"] == "Computer Science"


@pytest.mark.django_db
def test_user_cannot_set_another_user():
    """Test that user field is read-only and set automatically"""
    user = User.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    other_user = User.objects.create_user(
        username="otheruser", email="other@example.com", password="testpass123"
    )

    client = APIClient()
    client.force_authenticate(user=user)

    data = {
        "user": other_user.id,  # This should be ignored
        "major": "Computer Science",
        "year": "Junior",
    }
    resp = client.post("/api/profiles/", data)
    assert resp.status_code == status.HTTP_201_CREATED
    assert resp.json()["user"] == user.id  # Should be current user
    assert resp.json()["user"] != other_user.id


@pytest.mark.django_db
def test_user_can_only_see_own_profile():
    """Test that user can only see their own profile"""
    user = User.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    other_user = User.objects.create_user(
        username="otheruser", email="other@example.com", password="testpass123"
    )

    # Create profiles for both users
    Profile.objects.create(user=other_user, major="Physics", year="Senior")
    Profile.objects.create(user=user, major="CS", year="Junior")

    client = APIClient()
    client.force_authenticate(user=user)

    resp = client.get("/api/profiles/")
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.json()) == 1
    assert resp.json()[0]["user"] == user.id


@pytest.mark.django_db
def test_unauthenticated_bookmark_access():
    """Test that unauthenticated users get 403"""
    client = APIClient()
    resp = client.get("/api/bookmarks/")
    assert resp.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_authenticated_user_can_create_bookmark():
    """Test that authenticated user can create bookmark"""
    user = User.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    course = Course.objects.create(
        course_id="CS 225", dept="CS", title="Data Structures", credits=4
    )

    client = APIClient()
    client.force_authenticate(user=user)

    data = {"course": course.id}
    resp = client.post("/api/bookmarks/", data)
    assert resp.status_code == status.HTTP_201_CREATED
    assert resp.json()["user"] == user.id
    assert resp.json()["course"] == course.id


@pytest.mark.django_db
def test_user_can_only_see_own_bookmarks():
    """Test that user can only see their own bookmarks"""
    user = User.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    other_user = User.objects.create_user(
        username="otheruser", email="other@example.com", password="testpass123"
    )

    course1 = Course.objects.create(
        course_id="CS 225", dept="CS", title="Data Structures", credits=4
    )
    course2 = Course.objects.create(
        course_id="CS 374", dept="CS", title="Algorithms", credits=4
    )

    # Create bookmarks for both users
    Bookmark.objects.create(user=user, course=course1)
    Bookmark.objects.create(user=other_user, course=course2)

    client = APIClient()
    client.force_authenticate(user=user)

    resp = client.get("/api/bookmarks/")
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.json()) == 1
    assert resp.json()[0]["user"] == user.id
    assert resp.json()[0]["course"] == course1.id


@pytest.mark.django_db
def test_duplicate_bookmark_handling():
    """Test that duplicate bookmarks are handled gracefully"""
    user = User.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    course = Course.objects.create(
        course_id="CS 225", dept="CS", title="Data Structures", credits=4
    )

    # Create first bookmark
    Bookmark.objects.create(user=user, course=course)

    client = APIClient()
    client.force_authenticate(user=user)

    # Try to create duplicate
    data = {"course": course.id}
    resp = client.post("/api/bookmarks/", data)
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert "already bookmarked" in str(resp.json())


@pytest.mark.django_db
def test_courses_are_read_only():
    """Test that courses endpoint is read-only"""
    client = APIClient()

    # Test GET works
    resp = client.get("/api/courses/")
    assert resp.status_code == status.HTTP_200_OK

    # Test POST is not allowed
    data = {"course_id": "CS 999", "dept": "CS", "title": "Test Course", "credits": 3}
    resp = client.post("/api/courses/", data)
    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
def test_course_detail_access():
    """Test that course detail can be accessed"""
    course = Course.objects.create(
        course_id="CS 225", dept="CS", title="Data Structures", credits=4
    )

    client = APIClient()
    resp = client.get(f"/api/courses/{course.id}/")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["course_id"] == "CS 225"


@pytest.mark.django_db
def test_recommendations_requires_auth():
    client = APIClient()
    resp = client.get("/api/recommendations/")
    assert resp.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_recommendations_returns_courses_for_user():
    user = User.objects.create_user(
        username="testser", email="test@gmail.com", password="testpass123"
    )
    Course.objects.create(
        course_id="CS 225", dept="CS", title="Data Structures", credits=4
    )
    Course.objects.create(course_id="CS 374", dept="CS", title="Algorithms", credits=4)

    client = APIClient()
    client.force_authenticate(user=user)
    resp = client.get("/api/recommendations/")
    assert resp.status_code == status.HTTP_200_OK
    body = resp.json()
    assert "recommendations" in body
    assert len(body["recommendations"]) >= 1
