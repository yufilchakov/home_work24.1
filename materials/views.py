from datetime import datetime

from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.paginators import CoursePagination, LessonPagination
from materials.serializer import (CourseDetailSerializer, CourseSerializer,
                                  LessonSerializer, SubscriptionSerializer)
from materials.tasks import send_update_notification
from users.permissions import IsModerator, IsOwner


class CourseViewSet(ModelViewSet):
    """Класс является представлением API для управления курсами."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [~IsModerator]
        elif self.action in ["retrieve", "update"]:
            self.permission_classes = [IsAdminUser, IsModerator | IsOwner]
        elif self.action in ["destroy"]:
            self.permission_classes = [~IsModerator | IsOwner]
        return [permission() for permission in self.permission_classes]

    def form_valid(self, form):
        course = form.save()
        users = course.subscribers.all()
        if (
            not course.updated_at
            or (datetime.now() - course.updated_at).total_seconds() / 3600 > 4
        ):
            send_update_notification.delay(course, users)
        return super().form_valid(form)


class LessonCreateApiView(CreateAPIView):
    """Создание уроков."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]


class LessonListApiView(ListAPIView):
    """Список уроков."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator | IsOwner]
    pagination_class = LessonPagination


class LessonRetrieveApiView(RetrieveAPIView):
    """Информация об уроке по его идентификатору."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateApiView(UpdateAPIView):
    """Редактирование уроков."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    def form_valid(self, form):
        lesson = form.save()
        course = lesson.course
        users = course.subscribers.all()
        if (
            not lesson.updated_at
            or (datetime.now() - lesson.updated_at).total_seconds() / 3600 > 4
        ):
            send_update_notification.delay(course, users)
        return super().form_valid(form)


class LessonDestroyApiView(DestroyAPIView):
    """Удаление урока."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator | IsOwner]


class SubscriptionView(APIView):
    """Подписки на курсы."""

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def post(self, request):
        user = request.user
        course = request.data.get("course")
        course_item = get_object_or_404(Course, pk=course)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"

        return Response({"message": message})
