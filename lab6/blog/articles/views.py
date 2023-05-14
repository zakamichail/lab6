from django.http import HttpResponse, Http404
from .models import Article
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def home(request):
    return redirect('archive')
def archive(request):
    if not request.user.is_anonymous:
        return render(request, 'archive.html', {"posts": Article.objects.all(), "logged": True})
    else:
        return render(request, 'archive.html', {"posts": Article.objects.all(), "logged": False})
def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        if not request.user.is_anonymous:
            return render(request, 'article.html', {"post": post, "logged": True})
        else:
            return render(request, 'article.html', {"post": post, "logged": False})
    except Article.DoesNotExist:
        raise Http404

def create_post(request):
    if not request.user.is_anonymous:
        if request.method == "POST":
            # обработать данные формы, если метод POST
            form = {
                'text': request.POST["text"],
                'title': request.POST["title"],
            }
            # в словаре form будет храниться информация, введенная пользователем
            if form["text"] and form["title"]:
                # если поля заполнены без ошибок
                logic = bool(Article.objects.all().filter(title=form["title"]))
                if not logic:
                    Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                    arr = Article.objects.all()
                    return redirect('get_article', article_id=arr[len(arr) - 1].id)
                else:
                    form['errors'] = u"Такакя статья уже существует"
                    return render(request, 'create_post.html', {'form': form})
            # перейти на страницу поста
            else:
                # если введенные данные некорректны
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'create_post.html', {'form': form})
        else:
            # просто вернуть страницу с формой, если метод GET
            return render(request, 'create_post.html', {})
    else:
        raise Http404

def create_user(request):
    if request.method == "POST":
        # обработать данные формы, если метод POST
        form = {
            'login': request.POST["login"],
            'email': request.POST["email"],
            'password': request.POST["password"],
        }
        # в словаре form будет храниться информация, введенная пользователем
        if form["login"] and form["email"] and form["password"]:
            # если поля заполнены без ошибок
            try:
                User.objects.get(username=form["login"])
            # если пользователь существует, то ошибки не произойдет и программа
            # удачно доберется до следующей строчки
                form['errors'] = u"Такой пользователь уже существует"
                return render(request, 'create_user.html', {'form': form})
            except User.DoesNotExist:
                User.objects.create_user(form["login"], form["email"], form["password"])
                return redirect('archive')
            # перейти на страницу поста
        else:
            # если введенные данные некорректны
            form['errors'] = u"Не все поля заполнены"
            return render(request, 'create_user.html', {'form': form})
    else:
        # просто вернуть страницу с формой, если метод GET
        return render(request, 'create_user.html', {})

def user_login(request):
    if request.method == "POST":
        # обработать данные формы, если метод POST
        form = {
            'login': request.POST["login"],
            'password': request.POST["password"],
        }
        # в словаре form будет храниться информация, введенная пользователем
        if form["login"] and form["password"]:
            # если поля заполнены без ошибок
            try:
                User.objects.get(username=form["login"])
                # если пользователь существует, то ошибки не произойдет и программа
                # удачно доберется до следующей строчки
                #try:
                user = authenticate(username=form["login"], password=form["password"])
                if user is not None:
                    login(request, user)
                    return redirect('archive')
                else:
                    form['errors'] = u"Неверный пароль"
                    return render(request, 'login.html', {'form': form})

            except User.DoesNotExist:
                form['errors'] = u"Такого пользователя не существует"
                return render(request, 'login.html', {'form': form})
            # перейти на страницу поста
        else:
            # если введенные данные некорректны
            form['errors'] = u"Не все поля заполнены"
            return render(request, 'login.html', {'form': form})
    else:
        # просто вернуть страницу с формой, если метод GET
        return render(request, 'login.html', {})
def user_logout(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))