from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comments
from .forms import PostForm, CommentForm, ContactUsForm
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.contrib import messages
from .tasks import send_mail as celery_send_mail
from django.template.loader import render_to_string
from django.http import JsonResponse

from blog.serializers import PostSerializer, CommentsSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.published_date = timezone.now()
            post.save()
            subject = 'New post'
            message = 'New post was added'
            from_email = 'no_reply@somecompany.com'
            to_email = ['admin@somecompany.com']
            celery_send_mail.delay(subject, message, from_email, to_email)
            messages.add_message(request, messages.SUCCESS, 'Post added')
            return redirect('blog:posts_all')
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_l = post.comments_set.filter(published=True).all()
    paginator = Paginator(comment_l, 2)
    page = request.GET.get('page')
    comment_p = paginator.get_page(page)
    return render(request, 'blog/post_detail.html', {'post': post, 'comment': comment_p})


# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'post_detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(PostDetailView, self).get_context_data(**kwargs)
#         post = self.get_object()
#         comment = post.comments_set.filter(published=True).all()
#         paginator = Paginator(comment, 2)
#         context['comments'] = paginator.get_page(comment)
#         return context

    # def get_context_data(self):
    #     context = super(PostDetailView, self).get_context_data()
    #     _list = Comment.objects.filter(post=self.kwargs.get('pk'))
    #     paginator = Paginator(_list, 25) # Show 25 contacts per page
    #     page = request.GET.get('page')
    #     context['comments'] = paginator.get_page(page)
    #     return context


# @method_decorator(cache_page(10), 'dispatch')
class PostsListView(ListView):
    model = Post
    fields = ['title', 'text']
    queryset = Post.objects.filter(published=True)
    paginate_by = 10
    template_name = 'blog/posts_all.html'

    def get_object(self, **kwargs):
        user = self.request.user
        return user


class LoginUserPostsAllView(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 10
    template_name = 'blog/user_posts.html'

    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)

    def get_object(self, **kwargs):
        user = self.request.user
        return user


class UserPostDetailView(DetailView):
    model = Post
    template_name = 'blog/user_post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(UserPostDetailView, self).get_context_data(**kwargs)
        post = self.get_object()
        context['comment'] = post.comments_set.filter(published=True).all()
        return context


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'text', 'published']
    template_name = 'blog/post_update.html'
    success_url = reverse_lazy('blog:user_posts')

    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('blog:user_posts')
    login_url = reverse_lazy('registration:login')


class CommentAddView(LoginRequiredMixin, CreateView):
    model = Comments
    form_class = CommentForm
    template_name = 'blog/comment_add.html'
    login_url = reverse_lazy('user_management:login')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.post_id = self.kwargs['pk']
        subject = 'New comment'
        message = 'New comment was added'
        from_email = 'no_reply@somecompany.com'
        to_email = ['admin@somecompany.com']
        celery_send_mail.delay(subject, message, from_email, to_email)
        messages.add_message(self.request, messages.SUCCESS, 'Comment will be added after moderation')
        return super().form_valid(form)

    success_url = reverse_lazy('blog:posts_all')


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comments
    fields = ['text', 'published']
    template_name = 'blog/comment_update.html'
    success_url = reverse_lazy('blog:user_posts')

    def get_queryset(self):
        return Comments.objects.filter(owner=self.request.user)


class CommentsListView(ListView):
    model = Comments
    fields = ['user', 'text']
    queryset = Comments.objects.filter(published=True)
    paginate_by = 10
    template_name = 'blog/comments_all.html'

    def get_object(self, **kwargs):
        user = self.request.user
        return user


class LoginUserCommentsAllView(LoginRequiredMixin, ListView):
    model = Comments
    paginate_by = 10
    template_name = 'blog/user_comments_all.html'

    def get_queryset(self):
        return Comments.objects.filter(owner=self.request.user)

    def get_object(self, **kwargs):
        user = self.request.user
        return user


class UserCommentDetailView(DetailView):
    model = Comments
    template_name = 'blog/user_comment_detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super(UserCommentDetailView, self).get_context_data(**kwargs)
    #     post = self.get_object()
    #     return context


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comments
    template_name = 'blog/delete_comment.html'
    success_url = reverse_lazy('blog:user_comments')
    login_url = reverse_lazy('registration:login')


def contact_us_view(request):
    data = dict()
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = form.cleaned_data['from_email']
            to_email = ['admin@somecompany.com']
            celery_send_mail.delay(subject, message, from_email, to_email)
            # messages.add_message(request, messages.SUCCESS, 'Your message was sent successful')
            data['form_is_valid'] = True
            data['html_contact_us_success'] = render_to_string('blog/contact_us_success.html')
        else:
            data['form_is_valid'] = False
    else:
        form = ContactUsForm()
    context = {'form': form}
    data['html_form'] = render_to_string('blog/contact_us.html', context, request=request)
    return JsonResponse(data)


# def contact_us_view(request):
#     if request.method == "POST":
#         form = ContactUsForm(request.POST)
#         if form.is_valid():
#             subject = form.cleaned_data['subject']
#             message = form.cleaned_data['message']
#             from_email = form.cleaned_data['from_email']
#             to_email = ['admin@somecompany.com']
#             celery_send_mail.delay(subject, message, from_email, to_email)
#             messages.add_message(request, messages.SUCCESS, 'Message sent')
#             return redirect('blog:posts_all')
#     else:
#         form = ContactUsForm()
#     return render(request, "contact_us.html", context={"form": form})

class PostViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        post = self.get_object()
        return Response(post.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentsViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        comments = self.get_object()
        return Response(comments.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
