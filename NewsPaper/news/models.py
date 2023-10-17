from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.PROTECT)

    def update_rating(self):
        rating_of_post_by_author = Post.objects.filter(author=self).aggregate(Sum('rating'))['rating__sum'] * 3
        rating_of_comments_by_author = Comment.objects.filter(user=self.user).aggregate(Sum('rating'))['rating__sum']
        rating_of_comments_under_posts_of_author = Comment.objects.filter(post__author__user=self.user).aggregate(Sum('rating'))['rating__sum']
        self.rating = rating_of_post_by_author + rating_of_comments_by_author + rating_of_comments_under_posts_of_author

        self.save()


class Post(models.Model):
    article = 'AR'
    news = 'NE'

    TYPE_POSTS = [
        ('article', 'статья'),
        ('news', 'новости')
    ]

    articles_or_news = models.CharField(max_length=15, choices=TYPE_POSTS, default=article)
    text_articles_news = models.CharField(max_length=4500)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField('Category', through='PostCategory')
    title_articles_news = models.CharField(max_length=100)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text_articles_news[0:124] + '...'

    def __str__(self):
        return self.title_articles_news


class Category(models.Model):
    name_of_category = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name_of_category.title()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text_comment = models.CharField(max_length=1000)
    date_time_comment = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
