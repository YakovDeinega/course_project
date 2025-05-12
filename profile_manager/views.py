from django import urls
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter

from profile_manager.forms import LoginForm, RegisterForm, UserInformationForm
from profile_manager.models import UserInformation
from profile_manager.serializers import UserInformationSerializer


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(form.cleaned_data)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(email=cd['email'], password=cd['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(request.GET.get('next'), status=200)
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'profile_manager/login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cd['username'] = cd['email']
            del cd['password_again']
            user = User.objects.create_user(**cd)
            login(request, user)
            return redirect(urls.reverse(get_concrete_profile, args=[user.id]))
    else:
        form = RegisterForm()
    return render(request, 'profile_manager/register.html', {'form': form})


def get_concrete_profile(request, user_id: int):
    user = get_object_or_404(User, pk=user_id)
    needed_userInformation = UserInformation.objects.filter(user__id=user_id).first()
    if needed_userInformation:
        form = UserInformationForm(instance=needed_userInformation)
    else:
        form = UserInformationForm()
    name = f'{user.first_name} {user.last_name}'
    return render(request, 'profile_manager/profile.html', {'form': form, 'name': name})


class UserInformationListAPIView(generics.ListAPIView):
    queryset = UserInformation.objects.select_related('user').all()
    serializer_class = UserInformationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['town__name']
    search_fields = ['user__first_name', 'user__last_name']
    template_name = 'profile_manager/list_of_profiles.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        return render(request, self.template_name, {'users': response.data})
