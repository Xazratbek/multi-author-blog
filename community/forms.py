from django import forms
from .models import Community, CommunityMembership, CommunityMessages

class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['name', 'description']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            raise forms.ValidationError("Hamjamiyat nomi kamida 3-ta belgidan iborat bo'lsin")
        return name

    def clean_description(self):
        desc = self.cleaned_data.get('description')
        if len(desc) < 10:
            raise forms.ValidationError("Hamjamiyat uchun izox juda kam 10-belgidan ko'roq bo'lsin")
        return desc
