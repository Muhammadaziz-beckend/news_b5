from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from pprint import pprint
from news.models import Category, News, Tag
from workspace.decorators import is_owner
from workspace.forms import LoginForm, NewsForm, NewsModelForm, RegisterForm
from pprint import pprint
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required(login_url='/workspace/login/')
def workspace(request):
    news = News.objects.filter(author=request.user).order_by('-date', 'name')
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 4))
 
    pagin = Paginator(news, page_size)
    news = pagin.get_page(page) 

    return render(request, 'workspace/index.html', {'news': news})


@login_required(login_url='/workspace/login/')
def create_news(request):
    form = NewsModelForm()

    if request.method == 'POST':
        form = NewsModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return redirect('/workspace/')
         
    return render(request, 'workspace/create_news.html', {'form': form})


@login_required(login_url='/workspace/login/')
@is_owner
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


@login_required(login_url='/workspace/login/')
@is_owner
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


def login_profile(request):
    if request.user.is_authenticated:
        return redirect('/workspace/')
    
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)   
                return redirect('/workspace/') 
            

            message = 'The user does not exist or the password is incorrect.'
            return render(request, 'auth/login.html', {'form': form, 'message': message})


    return render(request, 'auth/login.html', {'form': form})



def logout_profile(request):
    if request.user.is_authenticated:
        logout(request)
    
    return redirect('/')


def register(request):
    if request.user.is_authenticated:
        return redirect('/workspace/')
    
    form = RegisterForm()

    
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/workspace/')
    

    return render(request, 'auth/register.html', {'form': form})
    


# Create your views here.
