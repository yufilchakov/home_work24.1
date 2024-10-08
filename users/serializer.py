from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class UserSerializer(ModelSerializer):
    """Реализация сериализатора для пользователя."""

    class Meta:
        model = User
        fields = "__all__"


class PaymentSerializer(ModelSerializer):
    """Реализация сериализатора для платежей."""

    class Meta:
        model = Payment
        fields = "__all__"
