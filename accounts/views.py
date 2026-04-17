from django.shortcuts import render, get_object_or_404
from .models import CustomUser, Profile
from .forms import CustomUserCreationForm, ProfileUpdateForm
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'username': self.object.username})

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'accounts/profile.html'
    context_object_name = 'profile'
    slug_field = 'user__username'
    slug_url_kwarg = 'username'

class ProfileListView(ListView):
    model = Profile
    template_name = 'accounts/profiles.html'
    context_object_name = 'profiles'

class MyProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/my_profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

class ProfileUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'accounts/update_profile.hmtl'
    context_object_name = 'profile'

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user