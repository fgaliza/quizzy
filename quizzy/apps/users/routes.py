from rest_framework import routers

from .views import AppUserViewSet

app_name = 'users'

user_router = routers.DefaultRouter()
user_router.register(r'users', AppUserViewSet, basename='users')

urlpatterns = []
urlpatterns += user_router.urls
