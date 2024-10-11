from datetime import datetime, timedelta

from celery import shared_task
from django.core.mail import send_mail

from config import settings
from users.models import User


@shared_task
def send_update_notification(course, users):
    """Отправляет уведомление об обновлении курса на электронную почту пользователям."""
    subject = f"Обновление курса {course.name}"
    message = f"Курс {course.name} был обновлен. Пожалуйста, посетите курс для просмотра изменений."
    from_email = settings.EMAIL_HOST_USER
    for user in users:
        send_mail(subject, message, from_email, [user.email])


@shared_task
def block_inactive_users():
    """Заблокировать пользователей, которые не заходили в систему за последние 30 дней"""
    one_month_ago = datetime.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lte=one_month_ago, is_active=True)
    for user in inactive_users:
        user.is_active = False
        user.save()
