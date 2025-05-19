from django.shortcuts import render, redirect
from article.models import Article, Comment
from django.core.paginator import Paginator

def index(request):
    articles = Article.objects.all().order_by('-id')
    
    paginator = Paginator(articles, 10)  # 페이지당 10개
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'index.html', {'page_obj': page_obj})

def show(request, pk):
    article = Article.objects.get(pk=pk)
    
    if request.method == 'POST':
        comment = Comment()
        comment.article = article
        comment.author = request.user
        comment.content = request.POST['content']
        comment.save()
        return redirect('article:show', pk=pk)

    comments = article.comments.all()
    return render(request, 'show.html', {'article': article, 'comments': comments})

def new(request):
    return render(request, 'new.html')

def create(request):
    if request.method == 'POST':
        article = Article()
        article.author = request.user
        article.title = request.POST['title']
        article.content = request.POST['content']
        article.save()
        return redirect('article:show', pk=article.pk)
        
    else:
        return render(request, 'new.html')

def edit(request, pk):
    article = Article.objects.get(pk=pk)
    
    return render(request, 'edit.html', {"article" : article})

def update(request, pk):
    article = Article.objects.get(pk=pk)
    
    if article.author != request.user:
        return redirect('article:show', pk=pk)
    
    article.title = request.POST['title']
    article.content = request.POST['content']
    article.save()
    
    return redirect('article:show', pk=article.pk)

def delete(request, pk):
    article = Article.objects.get(pk=pk)
    
    if article.author != request.user:
        return redirect('article:show', pk=pk)
    
    article.delete()
    
    return redirect('article:index')