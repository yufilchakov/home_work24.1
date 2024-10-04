from rest_framework.routers import SimpleRouter
from django.urls import path
from users.apps import UsersConfig
from users.views import PaymentViewSet, UserCreateApiView, UserListApiView, UserRetrieveApiView, UserUpdateApiView, \
    UserDestroyApiView

app_name = UsersConfig.name

router = SimpleRouter()
router.register("", PaymentViewSet)

urlpatterns = [
    path("users/", UserListApiView.as_view(), name="users_list"),
    path("users/create/", UserCreateApiView.as_view(), name="users_create"),
    path("users/<int:pk>/", UserRetrieveApiView.as_view(), name="users_retrieve"),
    path("users/<int:pk>/update/", UserUpdateApiView.as_view(), name="users_update"),
    path("users/<int:pk>/delete/", UserDestroyApiView.as_view(), name="users_delete"),
]

urlpatterns += router.urls
