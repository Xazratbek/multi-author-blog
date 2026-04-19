from django.shortcuts import render, get_object_or_404
from .models import CustomUser, Profile, AuthorFollow
from .forms import CustomUserCreationForm, ProfileUpdateForm
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.http import JsonResponse


class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse_lazy('my_profile')

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'accounts/profile.html'
    context_object_name = 'profile'
    slug_field = 'user__username'
    slug_url_kwarg = 'username'

    def get_queryset(self):
        user = get_object_or_404(CustomUser,username=self.kwargs.get("username"))
        Profile.objects.get_or_create(user=user, defaults={'bio': ''})
        return Profile.objects.filter(user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_following_author'] = (
            self.request.user.is_authenticated
            and self.request.user != self.object.user
            and AuthorFollow.objects.filter(user=self.request.user, author=self.object.user).exists()
        )
        return context

class ProfileListView(ListView):
    model = Profile
    template_name = 'accounts/profiles.html'
    context_object_name = 'profiles'

class MyProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/my_profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        profile, _ = Profile.objects.get_or_create(user=self.request.user, defaults={'bio': ''})
        return profile

class ProfileUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'profile'

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('my_profile')

class FollowToAuthorView(LoginRequiredMixin,View):
    def post(self, request, username):
        author = get_object_or_404(CustomUser,username=username)
        if author == request.user:
            return JsonResponse({"status": 400, 'message': "O'zingizga obuna bo'la olmaysiz"})
        _follow, created = AuthorFollow.objects.get_or_create(
            user=request.user, author=author
        )
        if not created:
            return JsonResponse({"status": 400,'message': 'Siz allaqachon bu muallifga obuna bo\'lgansiz', 'followers_count': author.followers.count()})

        return JsonResponse({"status": 201,'message':'Obuna bo\'ldingiz', 'followers_count': author.followers.count()})

class UnFollowView(LoginRequiredMixin, View):
    def post(self, request, username):
        author = get_object_or_404(CustomUser,username=username)
        follower = AuthorFollow.objects.filter(user=request.user,author=author).first()
        if follower and author.followers.filter(user=request.user).exists():
            follower.delete()
            return JsonResponse({"status": 200,'message':'Obuna bekor qilindi', 'followers_count': author.followers.count()})

        return JsonResponse({"status": 400, 'messsage': "Siz bu muallifga obuna bo'lmagansiz"})

class MyFollowersView(LoginRequiredMixin, View):
    def get(self, request):
        author = get_object_or_404(CustomUser, username=request.user.username)

        return render(request,'accounts/my_followers.html',context={"followers": author.followers.select_related('user'), "page_title": "Mening followerlarim"})

class MyFollowingsView(LoginRequiredMixin, View):
    def get(self, request):
        user = get_object_or_404(CustomUser, username=request.user.username)

        return render(request,'accounts/my_followers.html',context={"followers": user.followings.select_related('author'), "page_title": "Men obuna bo'lganlar", "is_followings": True})
