from django.contrib import admin

from .models import Article, Category, Comments



@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['user','article','content']
    fields = ['content','user','article']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
  
@admin.register(Article,)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title','user','slug','created','updated']
    search_fields = ['user','title']
    fields = ['title','slug','content','user','category','likes']
    list_select_related = ['user']
   