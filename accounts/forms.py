from .models import CustomUser, Profile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("email", "first_name", "last_name")

class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','age','avatar','telegram_url','instagram_url','linkedin_url','github_url']
