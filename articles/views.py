from django.core.paginator import Paginator
from django.contrib.messages import add_message,SUCCESS
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden 
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.urls import reverse
from .models import Article, Comments
from .forms import ArticleForm,ArticleTry, CategoryForm,CommentForm



def list_try(request):

    article_list = Article.objects.all()
    paginator = Paginator(article_list,10,allow_empty_first_page=False)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'articles':article_list,'title':'Articles','page_obj':page_obj}
    return render(request,'articles/list_view.html',context)

@login_required
def add_comment(request,article,user):
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = article
        comment.user = user
        comment.save()

def comment_delete(request,id):
    comment = Comments.objects.get(id=id)
    article = comment.article
    context = {'title':'comment delete','article':article,'object':comment}
    if request.POST:
        comment.delete()
        add_message(request,SUCCESS,'Comment deleted successfully')
        return redirect(article.get_absolute_url())
    return render(request,'articles\delete_confirm.html',context)


@login_required
def like(request,article,context):
    if not article.is_liked(request.user):
            article.likes.add(request.user)
            context['liked'] = True
            add_message(request,SUCCESS,'You liked the article')
    else:
        article.likes.remove(request.user)
        context['liked'] = False
        add_message(request,SUCCESS,'You unliked the article')

def detail_try(request,slug):
    article = get_object_or_404(Article,slug=slug)
    comment_form = CommentForm(request.POST or None)
    comments = Comments.objects.filter(article=article)

    context = {'article':article,'title':article.title,'comment_form':comment_form,'comments':comments}

    if request.user.is_authenticated:
       context['liked'] =  article.is_liked(request.user)

    
    if comment_form.is_valid() and 'comment' in request.POST :
            add_comment(request,article,request.user)
            return redirect(article.get_absolute_url())
    elif request.method == "POST" and 'Like' in request.POST:
        like(request,article,context)
        return redirect(article.get_absolute_url())


    return render(request,'articles/detail_view.html',context)


   


@login_required
def create_try(request):
    
    form = ArticleForm(request.POST or None)
    c_form = CategoryForm(request.POST or None)
    context = {'form':form,'title':'Create article',"c_form":c_form}

    if form.is_valid():
        article =  form.save(commit=False)
        article.user = request.user
        article.save()
        if 'category' in request.POST:
            category = request.POST['category']
            article.category.add(category)
        
        # print(c_form.is_valid())
        if c_form.is_valid():
            cat = c_form.save(commit=False)
            cat.save()
            article.category.add(cat)

        add_message(request,SUCCESS,'Article created')
        return redirect(article.get_absolute_url())

    return(render(request,'articles/create_update.html',context))

    


# @user_passes_test()e
def update_try(request,slug):

    article = Article.objects.get(slug=slug)
    form = ArticleForm(request.POST or None ,instance=article)
    c_form = CategoryForm(request.POST or None)
    
    context = {'article':article,"c_form":c_form,'form':form,'title':f'update {article.title}'}
    if form.is_valid():
        form.save()
        if c_form.is_valid():
            cat = c_form.save(commit=False)
            cat.save()
            article.category.add(cat)
        return redirect(article.get_absolute_url())

    return render(request,'articles/create_update.html',context)



@login_required
def delete_try(request,slug):
    article = Article.objects.get(slug=slug)
    context = {'title':'article delete','article':article,'object':article}
    
    if request.POST:
        Article.objects.get(slug=slug).delete()
        add_message(request,SUCCESS,'Article deleted successfully')
        return redirect('articles:list_view')

    return render(request,'articles\delete_confirm.html',context)

      
@login_required
def create_try_old(request):
    form = ArticleTry
    context = {'form':form}

    if request.POST:
        form = ArticleTry(request.POST)
        context = {'form':form}
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            article  = Article.objects.create(title=title,content=content,user_id = request.user.id)
            context = {'article':article,'created' : True}

        return(render(request,'articles/create.html',context))

        # title = request.POST['title']
        # content = request.POST['content']
        
        # article  = Article.objects.create(title=title,content=content,user_id = request.user.id)
        
           
    return(render(request,'articles/create.html',context))

    
def qs_search(request):
    query = request.GET.get('q')
    queryset = Article.objects.search(query)

    ctx = {'articles':queryset,'title':'Search'}

    return render(request,'articles/search.html',ctx)


###############################################

def list_view(request):

    articles = Article.objects.order_by('-created')
    context = {'articles':articles,'title':'Articles'}
    return render(request,'articles/list_view.html',context)

def detail_view(request,id):
    try:
        article = Article.objects.get(pk=id)
        context = {'article':article,'title':article.title}
    except:
        return HttpResponse("Article not found")

    return render(request,'articles/detail_view.html',context)

@login_required
def update_view(request,id):
    form = ArticleForm
    article = Article.objects.get(pk=id)
    context = {'article':article,'form':form,'title':f'update {article.title}'}
   
    if request.POST:
        form = ArticleForm(request.POST,instance=article)
        if form.is_valid:
            form.save()
            return redirect(reverse('articles:list_view'))
    return render(request,'articles/update_view.html',context)


@login_required
def create_article(request):
     
    form = ArticleForm
    context = {'form':form}
    if request.POST:
        form = ArticleForm(request.POST,)
        if form.is_valid:
            form.save()
            return redirect(reverse('articles:list_view'))
    return(render(request,'articles/create.html',context))


@login_required
def delete_article(request,id):
    article = Article.objects.get(pk=id)
    context = {'article':article}
    if request.POST:
        Article.delete(article)
        return redirect(reverse('articles:list_view'))
    return render(request,'articles/delete_confirm.html',context)





