from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from pprint import pprint
from news.models import Category, News, Tag
from workspace.decorators import is_owner
from workspace.forms import ChangeProfileForm, ChangePsswordForm, LoginForm, NewsForm, NewsModelForm, RegisterForm
from pprint import pprint
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from workspace.filters import WorkspaceFilter as NewsFilter



@login_required(login_url="/workspace/login/")
def workspace(request):
    news = News.objects.filter(author=request.user).order_by("-date", "name")

    filterset = NewsFilter(data=request.GET, queryset=news)

    news = filterset.qs

    category_id = request.GET.get("category", 0)
    tags_id = request.GET.get("tags", 'tags=')
    date_id = request.GET.get("date", 'date=')
    is_published_id = request.GET.get("is_published", 'is_published=')

    arr = [
        ("category", category_id),
        ("tags", tags_id),
        ("date", date_id),
        ("is_published", is_published_id),
    ]

    obj = {}

    for i in arr:
        if i[1]:
            obj[i[0]] = i[1]

    text = ""
    for i in obj:
        if not text:
            text += f"?{i}={obj[i]}"
        else:
            text += f"&{i}={obj[i]}"
    if text:
        text += "&"

    page = int(request.GET.get("page", 1))
    page_size = int(request.GET.get("page_size", 4))

    pagin = Paginator(news, page_size)
    news = pagin.get_page(page)
    print(obj, text, "1111")
    return render(
        request,
        "workspace/index.html",
        {"news": news, "filterset": filterset, "obj": text},
    )


@login_required(login_url="/workspace/login/")
def create_news(request):
    form = NewsModelForm()

    if request.method == "POST":
        form = NewsModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            messages.success(
                request, f'The news "{news.name}" has been successfully added!'
            )
            return redirect("/workspace/?is_published=on")

    return render(request, "workspace/create_news.html", {"form": form})


@login_required(login_url="/workspace/login/")
@is_owner
def delete_news(request, id):
    news = get_object_or_404(News, id=id)
    news.delete()
    messages.success(request, f'The news "{news.name}" has been successfully deleted!')
    return redirect("/workspace/?is_published=on")


# def update_news(request, id):
#     news = get_object_or_404(News, id=id)
#     form = NewsForm(
#         initial={
#             'name': news.name,
#             'description': news.description,
#             'content': news.content,языковой
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


@login_required(login_url="/workspace/login/")
@is_owner
def update_news(request, id):
    news = get_object_or_404(News, id=id)
    form = NewsModelForm(instance=news)

    if request.method == "POST":
        form = NewsModelForm(data=request.POST, files=request.FILES, instance=news)

        if form.is_valid():
            form.save()
            messages.success(
                request, f'The news "{news.name}" has been successfully updated!'
            )
            return redirect("/workspace/?is_published=on")

    return render(
        request,
        "workspace/update_news.html",
        {
            "news": news,
            "form": form,
        },
    )


def login_profile(request):
    if request.user.is_authenticated:
        return redirect("/workspace/?is_published=on")

    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Welcome "{user.get_full_name()}"')
                return redirect("/workspace/")

            message = "The user does not exist or the password is incorrect."
            return render(
                request, "auth/login.html", {"form": form, "message": message}
            )

    return render(request, "auth/login.html", {"form": form})


def logout_profile(request):
    if request.user.is_authenticated:
        logout(request)

    messages.success(request, f"Good bye!")

    return redirect("/?is_published=on+to&dsfsd")


def register(request):
    if request.user.is_authenticated:
        return redirect("/workspace/?is_published=on")

    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(data=request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome "{user.get_full_name()}"')
            return redirect("/workspace/is_published=on")

        messages.error(request, f"Fix some errors below!")

    return render(request, "auth/register.html", {"form": form})


@login_required(login_url='/workspace/login/')
def profile(request):

    form = ChangeProfileForm(instance=request.user)

    if request.method == 'POST':
        form = ChangeProfileForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Successfully changed profile')
            return redirect('/workspace/')

    return render(request, 'auth/profile.html', {'form': form})


@login_required(login_url='/workspace/login/')
def change_password(request):

    form = ChangePsswordForm(user=request.user)

    if request.method == 'POST':

        form = ChangePsswordForm(user=request.user, data=request.POST)

        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')

            user = request.user
            user.set_password(new_password)
            user.save()

            login(request, user)

            messages.success(request, f'Successfully changed password')
            return redirect('/workspace/')
    
    return render(request, 'auth/change_password.html', {'form': form})

# Create your views here.
