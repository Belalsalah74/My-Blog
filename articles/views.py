from django.core.paginator import Paginator
from django.contrib.messages import add_message, SUCCESS
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseForbidden
from .models import Article, Category, Comment
from .forms import ArticleForm, CategoryForm, CommentForm


def category_list(request):
    qs = Category.objects.all()
    context = {'qs': qs}
    return render(request, 'articles/category_list.html', context)


def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    qs = category.article.all()
    context = {'qs': qs, 'category': category}

    return render(request, 'articles/category_detail.html', context)


def category_create(request):
    form = CategoryForm(request.POST or None)
    context = {'form': form}
    if form.is_valid():
        form.save()
        add_message(request, SUCCESS, 'Category created successfully')
        return redirect('articles:article-create')
    return render(request, 'articles/category_form.html', context)


def article_list(request):
    article_list = Article.objects.all()
    paginator = Paginator(article_list, 5, allow_empty_first_page=True)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'articles': article_list,
               'page_obj': page_obj}
    return render(request, 'articles/article_list.html', context)


# Add Comment
def add_comment(request, article, user):
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.user = user
        comment.save()

# Delete Comment


def comment_delete(request, id):
    comment = get_object_or_404(Comment, id=id)
    article = comment.article
    if request.POST:
        comment.delete()
        add_message(request, SUCCESS, 'Comment deleted successfully')
        return redirect(article.get_absolute_url())

# Udpdate Comment


def comment_update(request, id):
    comment = get_object_or_404(Comment, id=id)
    if request.user == comment.user or request.user.is_staff:
        article = comment.article
        form = CommentForm(request.POST or None, instance=comment)
        context = {'comment': comment,
                   'article': article, 'form': form}
        if form.is_valid():
            form.save()
            add_message(request, SUCCESS, 'Comment updated successfully')
            return redirect(article.get_absolute_url())
        return render(request, 'articles/comment_update.html', context)
    else:
        return HttpResponseForbidden(request)


# Article detail view
def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    comment_form = CommentForm(request.POST or None)
    comments = Comment.objects.filter(article=article)

    context = {'article': article, 'title': article.title,
               'comment_form': comment_form, 'comments': comments, 'like_button': 'like'}

    if article.is_liked_by_user(request):
        context['like_button'] = 'unlike'

    if comment_form.is_valid() and 'comment' in request.POST:
        add_comment(request, article, request.user)
        return redirect(article)

    if 'like' in request.POST:
        article.like_or_unlike(request)
        return redirect(article)

    return render(request, 'articles/article_detail.html', context)

# Article create view
@login_required
def article_create(request):

    form = ArticleForm(request.POST or None)

    context = {'form': form}

    if form.is_valid():
        article = form.save(commit=False)
        article.user = request.user
        article.save()
        if 'category' in request.POST:
            category = request.POST['category']
            article.category.add(category)

        add_message(request, SUCCESS, 'Article created successfully')
        return redirect(article.get_absolute_url())

    return (render(request, 'articles/article_form.html', context))

# Article create view


def article_update(request, slug):

    article = Article.objects.get(slug=slug)
    if request.user == article.user or request.user.is_staff:
        form = ArticleForm(request.POST or None, instance=article)
        c_form = CategoryForm(request.POST or None)

        context = {'article': article, "c_form": c_form,
                   'form': form, }
        if form.is_valid():
            form.save()
            if c_form.is_valid():
                cat = c_form.save(commit=False)
                cat.save()
                article.category.add(cat)
            return redirect(article.get_absolute_url())

        return render(request, 'articles/article_form.html', context)
    else:
        return HttpResponseForbidden(request)

# Article delete view


def article_delete(request, slug):
    article = Article.objects.get(slug=slug)
    if request.POST:
        article.delete()
        add_message(request, SUCCESS, 'Article deleted successfully')
        return redirect('articles:article-list')


# Article search
def article_search(request):
    query = request.GET.get('query')
    queryset = Article.objects.search(query)
    paginator = Paginator(queryset, 5, allow_empty_first_page=True)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'articles': queryset,
               'title': 'Search result', 'query': query, 'page_obj': page_obj}

    return render(request, 'articles/search.html', context)
