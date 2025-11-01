from django.core.management.base import BaseCommand
from api.models import Course


class Command(BaseCommand):
    help = "Seed the database with sample courses"

    def handle(self, *args, **options):
        courses_data = [
            {
                "course_id": "CS 225",
                "dept": "CS",
                "title": "Data Structures",
                "credits": 4,
            },
            {
                "course_id": "CS 374",
                "dept": "CS",
                "title": "Algorithms & Models of Computation",
                "credits": 4,
            },
            {
                "course_id": "CS 241",
                "dept": "CS",
                "title": "System Programming",
                "credits": 4,
            },
            {
                "course_id": "MATH 241",
                "dept": "MATH",
                "title": "Calculus III",
                "credits": 4,
            },
            {
                "course_id": "PHYS 211",
                "dept": "PHYS",
                "title": "University Physics: Mechanics",
                "credits": 4,
            },
            {
                "course_id": "CHEM 102",
                "dept": "CHEM",
                "title": "General Chemistry I",
                "credits": 3,
            },
            {
                "course_id": "ENG 100",
                "dept": "ENG",
                "title": "Introduction to Engineering",
                "credits": 1,
            },
            {
                "course_id": "CS 126",
                "dept": "CS",
                "title": "Software Design Studio",
                "credits": 3,
            },
        ]

        created_count = 0
        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                course_id=course_data["course_id"], defaults=course_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created course: {course.course_id} - {course.title}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Course already exists: {course.course_id} - {course.title}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully seeded {created_count} new courses")
        )
