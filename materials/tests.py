from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):
    """Тестирование CRUD уроков."""

    def setUp(self):
        self.user = User.objects.create(email="admin@example.com", password="123qwe")
        self.lesson = Lesson.objects.create(name="Урок по Python!", owner=self.user)
        self.course = Course.objects.create(
            name="Курс по Python!", lesson=self.lesson, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        url = reverse("materials:lessons_create")
        data = {"name": "Новый урок по Python!", "course": self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Lesson.objects.get(name="Новый урок по Python!").owner, self.user
        )

    def test_lesson_update(self):
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {"name": "Обновленный урок по Python!"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Lesson.objects.get(pk=self.lesson.pk).name, "Обновленный урок по Python!"
        )

    def test_lesson_delete(self):
        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("materials:lessons_list")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "picture": None,
                    "link": None,
                    "link_to_video": None,
                    "course": None,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(data, result)


class SubscriptionTestCase(APITestCase):
    """Тестирование подписки на курсы."""

    def setUp(self):
        self.user = User.objects.create(email="admin@example.com", password="123qwe")
        self.course = Course.objects.create(name="Курс по Python!", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        url = reverse("materials:subscription")
        data = {"course": self.course.pk}
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {"message": "Подписка добавлена"})

    def test_unsubscribe(self):
        url = reverse("materials:subscription")
        data = {"course": self.course.pk}
        self.client.post(url, data)
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {"message": "Подписка удалена"})
