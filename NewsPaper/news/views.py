from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView, View
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .models import Post, Category, Author
from .filters import PostFilter
from .forms import PostForm
from django.conf import settings
import datetime


class PostList(ListView):
    model = Post
    ordering = 'text_articles_news'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    ordering = '-text_articles_news'
    template_name = 'post.html'
    context_object_name = 'post'


class PostSearch(ListView):
    model = Post
    ordering = 'text_articles_news'
    template_name = 'post_search.html'
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        form.instance.author = self.request.Author.user
        today = datetime.date.today()
        time_limit = today - datetime.timedelta(days=1)
        limit_actions = len(Post.objects.filter(author=post.author, time_create__gt=time_limit))
        if limit_actions >= 3:
            return render(self.request, 'news_limit_3in1day.html')
        post.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['time_now'] = datetime.datetime.utcnow()
        context['how_many'] = 3 #len(Post.objects.filter(author=post.author, time_create__gt=limit))
        return context


class NewsPostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'news_update.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categories = 'news'
        return super().form_valid(form)


class ArticlePostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'article_update.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categories = 'article'
        return super().form_valid(form)


class NewsPostDelete(DeleteView):
    model = Post
    template_name = 'new_delete.html'
    success_url = reverse_lazy('posts_list')


class ArticlePostDelete(DeleteView):
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('posts_list')


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    user.save()
    return redirect('posts_list')


class CategoryView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(categories=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribes.all()
        context['category'] = self.category
        return context


@login_required
def subscribers(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribes.add(user)
    message = 'Вы успешно подписались на категорию '
    html_content = render_to_string('send_mail.html',
                                    {'category': category.name_of_category},
                                    )
    msg = EmailMultiAlternatives(
        subject=f'Здравствуй увожаемый {user}, ты подписался на свою любиую категорию {category}',
        body=message,
        from_email=settings.EMAIL_HOST_USER + '@yandex.ru',
        to=[user.email]
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

    return render(request, 'subscribes.html', {'category': category, 'message': message, 'user': user})


@login_required
def unsubscribeds(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribes.remove(user)
    message = 'Вы отписались от категории'

    return render(request, 'unsubskribes.html', {'message': message, 'category': category})
