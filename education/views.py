from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter

from education.models import Lesson
from education.serializers import LessonSerializer


# Create your views here.


# def get_concrete_profile(request, user_id: int):
#     lesson = get_object_or_404(Lesson, pk=user_id)
#     needed_userInformation = UserInformation.objects.filter(user__id=user_id).first()
#     if needed_userInformation:
#         form = UserInformationForm(instance=needed_userInformation)
#     else:
#         form = UserInformationForm()
#     name = f'{user.first_name} {user.last_name}'
#     return render(request, 'profile_manager/profile.html', {'form': form, 'name': name})


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.prefetch_related('lecture_set').all()
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', 'lecture_set__name']
    template_name = 'education/list_of_courses.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        return render(request, self.template_name, {'courses': response.data})
