from datetime import datetime

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import Post
from .filters import PostFilter
from .forms import PostForm


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


class NewsPostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.articles_or_news = 'news'
        return super().form_valid(form)


class ArticlePostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'article_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.articles_or_news = 'article'
        return super().form_valid(form)


class NewsPostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_update.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categories = 'news'
        return super().form_valid(form)


class ArticlePostUpdate(UpdateView):
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











