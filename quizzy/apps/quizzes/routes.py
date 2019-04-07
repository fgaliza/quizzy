from rest_framework_nested import routers

from .views import ChoiceViewSet, QuestionViewSet

app_name = "quizzes"

question_router = routers.DefaultRouter()
question_router.register(r'questions', QuestionViewSet, basename='questions')

choice_router = routers.NestedDefaultRouter(question_router, r'questions')
choice_router.register(r'choices', ChoiceViewSet, basename='choices')

urlpatterns = []
urlpatterns += question_router.urls
urlpatterns += choice_router.urls
