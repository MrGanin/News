from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from .models import Post, BaseRegisterForm, Category, Subscribe, Author
from .filters import PostFilter
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from app.celery.tasks import task_send_message


class PostList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        a = Post.objects.filter(pk=self.object.pk).values('category')[0]
        context = super().get_context_data(**kwargs)
        context['id'] = self.object.category.values('pk')
        context['category'] = a['category']
        return context

    def post(self, request, *args, **kwargs):
        subscribers = Subscribe(
            user_id = request.user.pk,
            category_id = request.POST['category_id']
        )
        subscribers.save()

        return redirect('news_detail')

    def get_object(self, *args, **kwargs):
        flag = 'news' if self.request.path == '/news/' else 'articles'
        obj = cache.get(f'{flag}-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'{flag}-{self.kwargs["pk"]}', obj)

        return obj


class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class CreatePost(CreateView): #PermissionRequiredMixin, LoginRequiredMixin
    form_class = PostForm
    model = Post
    template_name = 'createpost.html'
    permission_required = ('app.add_post')

    def get_success_url(self):
        reverse_page = 'news_detail' if self.request.path == '/news/create/' else 'articles_detail'
        return reverse_lazy(reverse_page, args=[self.object.pk])

    def form_valid(self, form):
        post = form.save(commit=False)
        post.it_news = True if self.request.path == '/news/create/' else False
        post.author = Author.objects.get(user_id=self.request.user.pk)
        task_send_message.delay()
        return super().form_valid(form)

class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'editpost.html'
    permission_required = ('app.change_post')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objectpk'] = f'/news/{self.object.pk}/update/'
        return context

class PostDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'deletepost.html'
    success_url = reverse_lazy('general')
    permission_required = ('app.delete_post')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objectpk'] = f'/news/{self.object.pk}/delete/'
        return context

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = 'general'

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context

@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user)
        Author.objects.create(user=user)
    return redirect('profile')


@login_required
def subscriber(request, pk):
    category = Category.objects.get(pk=pk)
    user = request.user
    category.subscribers.add(user)
    return redirect(request.META.get('HTTP_REFERER'))



@login_required
def unsubscriber(request, pk):
    category = Category.objects.get(pk=pk)
    user = request.user
    category.subscribers.remove(user)
    return redirect(request.META.get('HTTP_REFERER'))

class IndexView2(View):
    def get(self, request):
        printer.apply_async([10], countdown = 5)
        hello.delay()
        return HttpResponse('Hello!')