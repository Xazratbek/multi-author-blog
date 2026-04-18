from django.shortcuts import render, get_object_or_404
from .models import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import *
from django.views import View
from django.http import JsonResponse

class CommunityListView(ListView):
    model = Community
    template_name = 'community/list.html'
    context_object_name = 'communities'
    paginate_by = 24

    def get_queryset(self):
        return Community.objects.all().select_related('owner').prefetch_related('members').order_by('-created_at')

class CommunityDetailView(DetailView):
    model = Community
    template_name = 'community/detail.html'
    context_object_name = 'community'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Community.objects.filter(slug=self.kwargs.get('slug')).select_related('owner').prefetch_related('members','messages')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_member'] = self.request.user.is_authenticated and self.request.user.is_member_of(self.object)
        return context

class CommunityCreateView(LoginRequiredMixin,CreateView):
    model = Community
    form_class = CommunityForm
    template_name = 'community/create.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('community_detail', kwargs={'slug': self.object.slug})

class JoinCommunityView(LoginRequiredMixin, View):
    def post(self, request, slug):
        community = get_object_or_404(Community, slug=slug)
        if request.user.is_member_of(community):
            return JsonResponse({"status": 400, 'message':"Siz allaqachon hamjamiyat a'zosisiz"})

        if community.owner == request.user:
            return JsonResponse({"status": 400, 'message': 'Siz xamjamiyat egasisiz'})

        if community.owner != request.user:
            CommunityMembership.objects.create(user=request.user,community=community,role='member')
            return JsonResponse({"status": 201, 'message': "Siz muvaffaqiyatli hamjamiyatga a'zo bo'ldingiz"})


class LeaveCommunityView(LoginRequiredMixin, View):
    def post(self, request,slug):
        community = get_object_or_404(Community, slug=slug)
        if community.owner ==  request.user:
            return JsonResponse({"status": 400, 'message': 'Siz hamjamiyat egasi sifatida hamjamiyatni tark eta olmaysiz\n O\'chirish uchun o\'chirish tugmasini bosing'})

        if request.user.is_member_of(community):
            member = CommunityMembership.objects.filter(user=request.user,community=community).first()
            member.delete()
            return JsonResponse({'status': 204, 'message': 'Siz hamjamiyatni tark etdingiz'})
        else:
            return JsonResponse({"status": 400,'message': 'Siz hamjamiyat a\'zosi emassiz'})

class CommunityMessageSendView(LoginRequiredMixin,View):
    def post(self, request,slug):
        message = request.POST.get("message",'')
        if message:
            community = get_object_or_404(Community,slug=slug)
            if request.user.is_member_of(community):
                message = CommunityMessage.objects.create(community=community,author=request.user,content=message)
                return JsonResponse({'status': 201,'message':'ok', 'author': request.user.username, 'content': message.content, 'created_at': message.created_at.strftime("%d %b %Y %H:%M")})
            else:
                return JsonResponse({'status': 400,'message': 'Siz hamjamiyat a\'zosi emassiz\nXabar yozish uchun hamjamiyatga obuna bo\'ling'})
        else:
            return JsonResponse({"status":400,'message':'Bo\'sh xabar yozmang'})
