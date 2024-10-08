from django.db import models

from config import settings
from users.models import User


class Course(models.Model):
    """Модель курсов."""

    name = models.CharField(
        max_length=50, verbose_name="Название курса", help_text="Укажите название курса"
    )
    preview = models.ImageField(
        upload_to="materials/preview",
        blank=True,
        null=True,
        verbose_name="Картинка",
        help_text="Добавьте картинку",
    )
    description = models.TextField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Описание курса",
        help_text="Укажите описание курса",
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Пользователь",
        help_text="Укажите пользователя курсов",
    )
    link = models.URLField(
        blank=True,
        null=True,
        verbose_name="Ссылка на видео",
        help_text="Укажите ссылку на видео",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    """Модель уроков."""

    name = models.CharField(
        max_length=50, verbose_name="Название урока", help_text="Укажите название урока"
    )
    description = models.TextField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Описание урока",
        help_text="Укажите описание урока",
    )
    picture = models.ImageField(
        upload_to="materials/picture",
        blank=True,
        null=True,
        verbose_name="Картинка",
        help_text="Добавьте картинку",
    )
    link_to_video = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Ссылка на видео",
        help_text="Укажите ссылку на видео",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Курс",
        help_text="Укажите курс",
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Пользователь",
        help_text="Укажите пользователя уроков",
    )
    link = models.URLField(
        blank=True,
        null=True,
        verbose_name="Ссылка на видео",
        help_text="Укажите ссылку на видео",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    """Модель подписок."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")

    def __str__(self):
        return f"{self.user} - {self.course.name}"
