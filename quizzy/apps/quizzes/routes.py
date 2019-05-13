from rest_framework_nested import routers

from .views import ChoiceViewSet, QuestionViewSet, QuizViewSet

app_name = "quizzes"

routes = routers.DefaultRouter()
routes.register(r'questions', QuestionViewSet, basename='questions')
routes.register(r'choices', ChoiceViewSet, basename='choices')
routes.register(r'quiz', QuizViewSet, basename='quiz')

urlpatterns = []
urlpatterns += routes.urls
