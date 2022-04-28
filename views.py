from articles.views import Article
from django.http import HttpResponse
from django.shortcuts import render


def welcome(request):
    articles = Article.objects.all()[:10]
    context = {'user':request.user,'articles':articles}
    return render(request,'homepage.html',context)



# def hello(request):
#     return HttpResponse("hello world")