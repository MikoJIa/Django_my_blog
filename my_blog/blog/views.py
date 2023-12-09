from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post


def post_list(request):
    post_list = Post.published.all()
    # Мы создаем экземпляр класса Paginator с числом объектов, возвращаемых в  расчете на страницу. Мы будем отображать по три поста на
    # страницу.
    paginator = Paginator(post_list, 3)
    # Мы извлекаем HTTP GET-параметр page и сохраняем его в переменной
    # page_number. Этот параметр содержит запрошенный номер страницы.
    # Если параметра page нет в GET-параметрах запроса, то мы используем
    # стандартное значение 1, чтобы загрузить первую страницу результатов.
    page_number = request.GET.get('page', 1)
    # Мы получаем объекты для желаемой страницы, вызывая метод page()
    # класса Paginator. Этот метод возвращает объект Page, который хранится
    # в переменной posts.
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page_number не целое число, то
        # выдать первую страницу
        posts = paginator.page(1)
    except EmptyPage:
    # Если page_number находится вне диапазона, то
    # выдать последнюю страницу
        posts = paginator.page(paginator.num_pages)
        # Мы получаем общее число страниц посредством paginator.num_pages.
    context = {
        'posts': posts
    }
    return render(request, 'blog/post/list.html', context)


def post_detail(request, year, month, day, post):
    try:
        post = get_object_or_404(Post,
                                 status=Post.Status.PUBLISHED,
                                 slug=post,
                                 publish__year=year,
                                 publish__month=month,
                                 publish__day=day)
    except Post.DoesNotExist:
        raise Http404('No post found')
    return render(request, 'blog/post/detail.html', {'post': post})
