from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        

class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')
    
    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    number_lessons = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')

    def get_number_lessons(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = ("name", "preview", "description", "lessons", "number_lessons")
