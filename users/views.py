from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.serializer import PaymentSerializer, UserSerializer
from users.services import (create_stripe_price, create_stripe_product,
                            create_stripe_session)


class UserCreateApiView(CreateAPIView):
    """Класс является представлением API для создания нового пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentViewSet(ModelViewSet):
    """Класс является представлением API для управления платежами."""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = (
        "payment_date",
        "payment_amount",
    )
    search_fields = ("payment_method",)
    filterset_fields = ("payment_date", "paid_course", "paid_lesson", "payment_method")


class PaymentCreateAPIView(CreateAPIView):
    """Класс является представлением API для создания нового платежа."""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save()
        payment.user = self.request.user
        stripe_product_id = create_stripe_product(payment)
        payment.amount = payment.payment_amount
        price = create_stripe_price(
            amount=payment.amount, stripe_product_id=stripe_product_id
        )
        session_id, payment_link = create_stripe_session(price=price)
        payment.session_id = session_id
        payment.payment_url = payment_link
        payment.save()
