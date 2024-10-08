from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_url


class LessonSerializer(serializers.ModelSerializer):
    """Реализация сериализатора для уроков."""

    validators = [validate_url]

    class Meta:
        validators = [validate_url]
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """Реализация сериализатора для курсов."""

    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")
    validators = [validate_url]
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        return Subscription.objects.filter(user=user, course=obj).exists()

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    """Реализация сериализатора для детальной информации о курсе."""

    number_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source="lesson_set")

    def get_number_lessons(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = ("name", "preview", "description", "lessons", "number_lessons")


class SubscriptionSerializer(serializers.ModelSerializer):
    """Реализация сериализатора для подписок."""

    class Meta:
        model = Subscription
        fields = "__all__"
