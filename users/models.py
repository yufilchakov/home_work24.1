from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""

    username = None

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    telephone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите номер телефона",
    )
    side = models.CharField(
        max_length=35,
        verbose_name="Страна",
        blank=True,
        null=True,
        help_text="Укажите страну",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    """Модель платежей."""

    payment_choices = {
        "cash": "наличные",
        "transfer": "перевод на счет",
    }

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    payment_date = models.DateField(verbose_name="Дата оплаты")
    paid_course = models.ForeignKey(
        "materials.Course",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Оплаченный курс",
    )
    paid_lesson = models.ForeignKey(
        "materials.Lesson",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Оплаченный урок",
    )
    payment_amount = models.PositiveIntegerField(default=0, verbose_name="Cумма оплаты")
    payment_method = models.CharField(
        max_length=20, choices=payment_choices, verbose_name="Метод оплаты"
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["-payment_date"]

    def __str__(self):
        return f"Пользователь {self.user} оплатил {self.payment_amount} - {self.payment_date}"
