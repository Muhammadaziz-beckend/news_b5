from django.http import Http404
from django.shortcuts import render, get_object_or_404
from news.models import News, Category
from django.core.paginator import Paginator

from workspace.filters import NewsFilter



def main(request):
    news = News.objects.filter(is_published=True)

    search = request.GET.get('search')
    
    if search:
        news = news.filter(name__icontains=search)

    category_id = request.GET.get('category')

    if category_id:
        news = news.filter(category__id=int(category_id))

    filterset = NewsFilter(data=request.GET, queryset=news)

    news = filterset.qs



    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 4))
 
    pagin = Paginator(news, page_size)
    news = pagin.get_page(page) 

    return render(request, 'index.html', {'news': news, 'filterset': filterset,})


def detail_news(request, id):
    # try:
    #     news = News.objects.get(id=id, is_published=True)
    # except News.DoesNotExist as e:
    #     raise Http404

    news = get_object_or_404(News, id=id)

    if request.user.is_authenticated:
        user = request.user
        if user != news.author:
            news.views += 1
    
    else:
        news.views += 1

    news.save()


    return render(request, 'detail_news.html', {'news': news})


# Create your views here.
