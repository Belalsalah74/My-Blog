from django.core.paginator import Paginator
from django.contrib.messages import add_message, SUCCESS
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Article, Comments
from .forms import ArticleForm, CategoryForm, CommentForm

def list_try(request):
    article_list = Article.objects.all()
    paginator = Paginator(article_list, 10, allow_empty_first_page=True)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'articles': article_list,
               'title': 'Articles', 'page_obj': page_obj}
    return render(request, 'articles/list_view.html', context)

# Add Comment
@login_required
def add_comment(request, article, user):
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.user = user
        comment.save()

# Delete Comment
def comment_delete(request, id):
    comment = Comments.objects.get(id=id)
    article = comment.article
    context = {'title': 'comment delete',
               'article': article, 'object': comment}
    if request.POST:
        comment.delete()
        add_message(request, SUCCESS, 'Comment deleted successfully')
        return redirect(article.get_absolute_url())
    return render(request, 'articles\delete_confirm.html', context)



# Article detail view
def detail_try(request, slug):
    article = get_object_or_404(Article, slug=slug)
    comment_form = CommentForm(request.POST or None)
    comments = Comments.objects.filter(article=article)

    context = {'article': article, 'title': article.title,
               'comment_form': comment_form, 'comments': comments, 'like_button':'like'}

    if article.is_liked_by_user(request):
        context['like_button'] = 'unlike'
    print(request.POST)
    if comment_form.is_valid() and 'comment' in request.POST:
        add_comment(request, article, request.user)
        
    elif 'like' in request.POST:
        article.like_or_unlike(request)

        return redirect(article.get_absolute_url())

    return render(request, 'articles/detail_view.html', context)

# Article create view
@login_required
def create_try(request):

    form = ArticleForm(request.POST or None)
    c_form = CategoryForm(request.POST or None)
    context = {'form': form, 'title': 'Create article', "c_form": c_form}

    if form.is_valid():
        article = form.save(commit=False)
        article.user = request.user
        article.save()
        if 'category' in request.POST:
            category = request.POST['category']
            article.category.add(category)

        
        if c_form.is_valid():
            cat = c_form.save(commit=False)
            cat.save()
            article.category.add(cat)

        add_message(request, SUCCESS, 'Article created')
        return redirect(article.get_absolute_url())

    return (render(request, 'articles/create_update.html', context))


def update_try(request, slug):

    article = Article.objects.get(slug=slug)
    form = ArticleForm(request.POST or None, instance=article)
    c_form = CategoryForm(request.POST or None)

    context = {'article': article, "c_form": c_form,
               'form': form, 'title': f'update {article.title}'}
    if form.is_valid():
        form.save()
        if c_form.is_valid():
            cat = c_form.save(commit=False)
            cat.save()
            article.category.add(cat)
        return redirect(article.get_absolute_url())

    return render(request, 'articles/create_update.html', context)


@login_required
def delete_try(request, slug):
    article = Article.objects.get(slug=slug)
    context = {'title': 'article delete',
               'article': article, 'object': article}

    if request.POST:
        Article.objects.get(slug=slug).delete()
        add_message(request, SUCCESS, 'Article deleted successfully')
        return redirect('articles:article-list')

    return render(request, 'articles\delete_confirm.html', context)


# Article search
def qs_search(request):
    query = request.GET.get('q')
    queryset = Article.objects.search(query)

    ctx = {'articles': queryset, 'title': 'Search'}

    return render(request, 'articles/search.html', ctx)

