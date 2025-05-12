from django.urls import path

from education import views
from education.views import LessonListAPIView

urlpatterns = [
    # post views
    path('', LessonListAPIView.as_view(), name='get_list_of_lessons'),
    # path('<int:user_id>/', views.get_concrete_course, name='get_concrete_course'),
]
