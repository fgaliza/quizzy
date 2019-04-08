from rest_framework_nested import routers

from .views import QuestionViewSet, ChoiceViewSet, QuizViewSet

app_name = "quizzes"

question_router = routers.DefaultRouter()
question_router.register(r'questions', QuestionViewSet, basename='questions')

choice_router = routers.NestedDefaultRouter(question_router, r'questions')
choice_router.register(r'choices', ChoiceViewSet, basename='choices')

quiz_router = routers.DefaultRouter()
quiz_router.register(r'quiz', QuizViewSet, basename='quiz')

urlpatterns = []
urlpatterns += question_router.urls
urlpatterns += choice_router.urls
urlpatterns += quiz_router.urls
