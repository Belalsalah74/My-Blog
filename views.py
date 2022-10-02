from articles.models import Article
from django.shortcuts import render


def welcome(request):
    articles = Article.objects.all()[:10]
    context = {'user': request.user, 'articles': articles}
    return render(request, 'articles/homepage.html', context)
