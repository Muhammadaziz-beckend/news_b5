from django.http import Http404
from django.shortcuts import render, get_object_or_404
from news.models import News, Category
from django.core.paginator import Paginator



def main(request):
    news = News.objects.filter(is_published=True)

    search = request.GET.get('search')
    
    if search:
        news = news.filter(name__icontains=search)

    category_id = int(request.GET.get('category', 0))

    if category_id:
        news = news.filter(category__id=category_id)

    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 4))
 
    pagin = Paginator(news, page_size)
    news = pagin.get_page(page) 

    return render(request, 'index.html', {'news': news})


def detail_news(request, id):
    # try:
    #     news = News.objects.get(id=id, is_published=True)
    # except News.DoesNotExist as e:
    #     raise Http404

    news = get_object_or_404(News, id=id)

    return render(request, 'detail_news.html', {'news': news})


# Create your views here.
