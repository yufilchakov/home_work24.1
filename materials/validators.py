from rest_framework.serializers import ValidationError

link = "https://www.youtube.com/"


def validate_url(value):
    if value.get("link"):
        if link not in value.get("link"):
            raise ValidationError(f"Разрешена только ссылка на youtube")
