from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
from django.views.generic import ListView

from .forms import EmailPostForm
from .models import Post


class PostListView(ListView):
    """Альтернативное представление списка постов"""
    queryset = Post.published.all()
    # атрибут queryset используется для того, чтобы иметь конкретно-прикладной набор запросов QuerySet, не извлекая все объекты. Вместо
    # определения атрибута queryset мы могли бы указать model=Post, и Django
    # сформировал бы для нас типовой набор запросов Post.objects.all();
    context_object_name = 'posts'
    # контекстная переменная posts используется для результатов запроса.
    # Если не указано имя контекстного объекта context_object_name, то по
    # умолчанию используется переменная object_list;
    paginate_by = 3
    template_name = 'blog/post/list.html'
    # конкретно-прикладной шаблон используется для прорисовки страницы
    # шаблоном template_name. Если шаблон не задан, то по умолчанию ListView будет использовать blog/post_list.html.



# def post_list(request):
#     post_list = Post.published.all()
#     # Мы создаем экземпляр класса Paginator с числом объектов, возвращаемых в  расчете на страницу. Мы будем отображать по три поста на
#     # страницу.
#     paginator = Paginator(post_list, 3)
#     # Мы извлекаем HTTP GET-параметр page и сохраняем его в переменной
#     # page_number. Этот параметр содержит запрошенный номер страницы.
#     # Если параметра page нет в GET-параметрах запроса, то мы используем
#     # стандартное значение 1, чтобы загрузить первую страницу результатов.
#     page_number = request.GET.get('page', 1)
#     # Мы получаем объекты для желаемой страницы, вызывая метод page()
#     # класса Paginator. Этот метод возвращает объект Page, который хранится
#     # в переменной posts.
#     try:
#         posts = paginator.page(page_number)
#     except PageNotAnInteger:
#         # Если page_number не целое число, то
#         # выдать первую страницу
#         posts = paginator.page(1)
#     except EmptyPage:
#     # Если page_number находится вне диапазона, то
#     # выдать последнюю страницу
#         posts = paginator.page(paginator.num_pages)
#         # Мы получаем общее число страниц посредством paginator.num_pages.
#     context = {
#         'posts': posts
#     }
#     return render(request, 'blog/post/list.html', context)


def post_share(request, post_id):
    # Извлечь пост по идентификатору id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        # Форма была передана на обработку
        form = EmailPostForm(request.POST)

        if form.is_valid():
            # Поля формы успешно прошли валидацию
            cd = form.cleaned_data
            # Если форма валидна, то валидированные данные извлекаются посредством form.cleaned_data.
            # Указанный атрибут представляет собой словарь
            # полей формы и их значений.
            # ... отправить электронное письмо
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{cd["name"]} recommends you read {post.title}'
            message = f'Read {post.title} at {post_url}\n\n ' \
                      f'{cd["name"]} s comments: {cd["comments"]}'
            send_mail(subject, message, 'mikolaypopov9@gmail.com', [cd["to"]])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


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


