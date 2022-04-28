from tabnanny import verbose
from unicodedata import category
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q
from django.db import models


    

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name


class ArticleQuerySet(models.QuerySet):
    def search(self,query=None):
        if query != ' ' and query is not None:    
            lookup = Q(title__icontains=query) | Q(content__icontains=query) | Q(user__username__iexact=query)
            return self.filter(lookup)

class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model,using=self.db)    
    
    def search(self,query):
        return self.get_queryset().search(query)

class Article(models.Model):
    objects = ArticleManager()
    title = models.CharField(max_length=255)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    published = models.DateField(auto_now=False,auto_now_add=False,blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    slug = models.SlugField(null=True,blank=True,)
    category = models.ManyToManyField(Category,blank=True,
    related_name='article')
    likes = models.ManyToManyField(User,related_name='likes')
    

    class Meta:
        ordering = ['-updated','-created']

    def is_liked(self,user):
        # user = request.user
        if user.likes.filter(id=self.id).exists():
            return True
        return False

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("articles:detail_view", kwargs={'slug':self.slug})
        
    # def save(self, *args, **kwargs):
    #     if self.slug is None:
    #         self.slug = slugify(self.title)
    #     super().save(*args , **kwargs)
    

# @receiver(pre_save,sender=Article)
# def article_pre_save(sender,instance,*args, **kwargs,):
#     if instance.slug is None:
#         instance.slug = slugify(instance.title)

class Comments(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    article = models.ForeignKey(Article,related_name='comments',on_delete=models.CASCADE)
    content = models.TextField(max_length=255,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return f'{self.user} - {self.article}'
    
    def __repr__(self) -> str:
        return 'comment'
    
    

    class Meta:
        ordering = ['created_at','article']
        verbose_name = 'comments'
        verbose_name_plural = 'comments'
