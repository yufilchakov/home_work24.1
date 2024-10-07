from django.core.management.base import BaseCommand

from materials.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user1, _ = User.objects.get_or_create(email="user1@example.com")
        user2, _ = User.objects.get_or_create(email="user2@example.com")

        course1 = Course.objects.create(name="Course 1")
        lesson1 = Lesson.objects.create(name="Lesson 1", course=course1)

        Payment.objects.create(
            user=user1,
            payment_date="2022-01-01",
            paid_course=course1,
            payment_amount=100.00,
            payment_method="cash",
        )
        Payment.objects.create(
            user=user2,
            payment_date="2022-01-15",
            paid_lesson=lesson1,
            payment_amount=50.00,
            payment_method="transfer",
        )
        Payment.objects.create(
            user=user1,
            payment_date="2022-02-01",
            paid_course=course1,
            payment_amount=150.00,
            payment_method="cash",
        )
