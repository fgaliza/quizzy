from rest_framework_nested import routers

from .views import QuestionViewSet

app_name = "quizzes"

question_router = routers.DefaultRouter()
question_router.register(r'questions', QuestionViewSet, basename='questions')

urlpatterns = []
urlpatterns += question_router.urls
