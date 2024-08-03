from django.shortcuts import get_object_or_404, redirect

from news.models import News


def is_owner(views):

    def inner_func(request, id, *args, **kwargs):
        news = get_object_or_404(News, id=id)

        if news.author == request.user:
            return views(request, id, *args, **kwargs)
        
        return redirect('/workspace/')

    return inner_func