from django.urls import path

from profile_manager import views
from profile_manager.views import UserInformationListAPIView

urlpatterns = [
    # post views
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('profiles/', UserInformationListAPIView.as_view(), name='get_list_of_profiles'),
    path('profiles/<int:user_id>/', views.get_concrete_profile, name='get_concrete_profile'),
]