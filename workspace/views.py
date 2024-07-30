from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from pprint import pprint
from news.models import Category, News, Tag
from workspace.forms import NewsForm, NewsModelForm
from pprint import pprint


def workspace(request):
    news = News.objects.all().order_by('-date', 'name')
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 4))
 
    pagin = Paginator(news, page_size)
    news = pagin.get_page(page) 

    return render(request, 'workspace/index.html', {'news': news})


def create_news(request):
    form = NewsModelForm()

    if request.method == 'POST':
        form = NewsModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            news = form.save()
            return redirect('/workspace/')
         
    return render(request, 'workspace/create_news.html', {'form': form})


def delete_news(request, id):
    news = get_object_or_404(News, id=id)
    news.delete()
    return redirect('/workspace/')


# def update_news(request, id):
#     news = get_object_or_404(News, id=id)
#     form = NewsForm(
#         initial={
#             'name': news.name,
#             'description': news.description,
#             'content': news.content,
#             'category': news.category,
#             'tags': news.tags.all(),
#             'author': news.author,
#             'is_published': news.is_published,

#         }
#     )

#     if request.method == 'POST':
#         form = NewsForm(data=request.POST, files=request.FILES)

#         if form.is_valid():
#             news.name = form.cleaned_data.get('name')
#             news.description = form.cleaned_data.get('description')
#             news.content = form.cleaned_data.get('content')
#             news.author = form.cleaned_data.get('author')
#             news.is_published = form.cleaned_data.get('is_published')
#             news.category = form.cleaned_data.get('category')
#             tags = form.cleaned_data.get('tags')

#             news.tags.clear()
#             news.tags.add(*tags)

#             image = form.cleaned_data.get('image')

#             if image:
#                 news.image.save(image.name, image)

#             news.save()
            
#             return redirect('/workspace/')

#     return render(request, 'workspace/update_news.html', {
#         'news': news,
#         'form': form,
#     })


def update_news(request, id):
    news = get_object_or_404(News, id=id)
    form = NewsModelForm(instance=news)

    if request.method == 'POST':
        form = NewsModelForm(data=request.POST, files=request.FILES, instance=news)

        if form.is_valid():
            form.save()
            return redirect('/workspace/')

    return render(request, 'workspace/update_news.html', {
        'news': news,
        'form': form,
    })



# Create your views here.
