from articles.views import Article
from django.shortcuts import render
from django.conf import settings


def welcome(request):
    articles = Article.objects.all()[:5]
    context = {'user':request.user,'articles':articles}
    return render(request,'homepage.html',context)

