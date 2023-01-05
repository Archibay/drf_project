from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.contrib.auth.views import FormView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from user_management.forms import RegistrationForm
from blog.models import Post


class RegistrationView(FormView):
    template_name = 'registration/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('blog:posts_all')

    def form_valid(self, form):
        user = form.save()
        user = authenticate(self.request, username=user.username, password=form.cleaned_data.get('password1'))
        login(self.request, user)
        return super(RegistrationView, self).form_valid(form)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'registration/user_detail.html'

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'registration/user_update.html'
    success_url = reverse_lazy('user_management:user_detail')

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class UserProfilePublicDetailView(DetailView):
    model = User
    template_name = 'registration/user_detail_public.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfilePublicDetailView, self).get_context_data(**kwargs)
        user = self.get_object()
        context['posts_count'] = user.post_set.filter(published=True).count()
        context['posts'] = user.post_set.filter(published=True)
        return context
