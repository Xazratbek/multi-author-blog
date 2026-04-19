from django.shortcuts import render, get_object_or_404
from .models import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import *
from django.views import View
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden

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
        if self.request.user.is_authenticated:
            is_member = self.request.user.is_member_of(self.object)
            is_owner = self.request.user == self.object.owner
        else:
            is_member = False
            is_owner = False
        
        context['is_member'] = is_member
        context['can_post_message'] = is_member or is_owner
        context['communities'] = Community.objects.order_by('-created_at')
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


class CommunityMessageListView(LoginRequiredMixin, View):
    def get(self, request, slug):
        community = get_object_or_404(Community, slug=slug)
        if not (request.user.is_member_of(community) or community.owner == request.user):
            return HttpResponseForbidden()

        last_message_id = request.GET.get('last_message_id')
        if last_message_id:
            messages = community.messages.filter(id__gt=last_message_id).order_by('created_at')
            return render(request, 'community/partials/message_list.html', {'messages': messages})
        
        return HttpResponse('')


class CommunityMessageSendView(LoginRequiredMixin,View):
    def post(self, request,slug):
        message_content = request.POST.get("message",'').strip()
        if message_content:
            community = get_object_or_404(Community,slug=slug)
            if request.user.is_member_of(community) or community.owner == request.user:
                new_message = CommunityMessage.objects.create(
                    community=community,
                    author=request.user,
                    content=message_content
                )
                return render(request, 'community/partials/message_list.html', {'messages': [new_message]})
            else:
                return HttpResponseForbidden("You are not authorized to post in this community.")
        else:
            return HttpResponse('')
