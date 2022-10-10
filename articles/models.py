from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q
from django.db import models
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("articles:category-detail", kwargs={'pk': self.id})


class ArticleQuerySet(models.QuerySet):
    def search(self, query=None):
        if query != ' ' and query is not None:
            lookup = Q(title__icontains=query) | Q(
                content__icontains=query) | Q(user__username__iexact=query)
            return self.filter(lookup)


class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self.db)

    def search(self, query):
        return self.get_queryset().search(query)


class Article(models.Model):
    objects = ArticleManager()
    title = models.CharField(max_length=255)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(null=True, blank=True,)
    category = models.ManyToManyField(Category, blank=True,
    related_name='article')
    likes = models.ManyToManyField(User, related_name='likes')

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.title
        
    def is_liked_by_user(self,request):
        user = request.user
        if self.likes.filter(id=user.id):
            return True
        return False


    @method_decorator(login_required)
    def like_or_unlike(self, request):
        user = request.user
        if self.is_liked_by_user(request):
            self.likes.remove(user.id)
        else:
            self.likes.add(user.id)

    def get_absolute_url(self):
        return reverse("articles:article-detail", kwargs={'slug': self.slug})
        
 

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    article = models.ForeignKey(Article,related_name='comments',on_delete=models.CASCADE)
    content = models.TextField(validators=[MinLengthValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return f'{self.user} - {self.article}'
    
    def __repr__(self) -> str:
        return 'comment'
    
    

    class Meta:
        ordering = ['-created_at','article']
        verbose_name = 'comment'
