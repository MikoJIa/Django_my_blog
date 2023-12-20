from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
from django.views.generic import ListView

from .forms import EmailPostForm, CommentForm
from .models import Post, Comment
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count  # Это функция агрегирования Count из Django ORM-преобразователя. Данная
     #  функция позволит выполнять агрегированный подсчет тегов.


# class PostListView(ListView):
#     """Альтернативное представление списка постов"""
#     queryset = Post.published.all()
#     # атрибут queryset используется для того, чтобы иметь конкретно-прикладной набор запросов QuerySet, не извлекая все объекты. Вместо
#     # определения атрибута queryset мы могли бы указать model=Post, и Django
#     # сформировал бы для нас типовой набор запросов Post.objects.all();
#     context_object_name = 'posts'
#     # контекстная переменная posts используется для результатов запроса.
#     # Если не указано имя контекстного объекта context_object_name, то по
#     # умолчанию используется переменная object_list;
#     paginate_by = 3
#     template_name = 'blog/post/list.html'
    # конкретно-прикладной шаблон используется для прорисовки страницы
    # шаблоном template_name. Если шаблон не задан, то по умолчанию ListView будет использовать blog/post_list.html.



def post_list(request, tag_slug=None):  # tag_slug - этот параметр будет передан в url-адресе.
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    # Мы создаем экземпляр класса Paginator с числом объектов, возвращаемых в  расчете на страницу. Мы будем отображать по три поста на
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
        'posts': posts,
        'tag': tag
    }
    return render(request, 'blog/post/list.html', context)


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

    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # Список активных комментариев к этому посту
    # мы добавили набор запросов QuerySet, чтобы извлекать все активные
    # комментарии к посту, как показано ниже
    comments = post.comments.filter(active=True)
    # Форма для комментирования пользователями
    form = CommentForm()
    #  список схожих постов
    post_tags_ids = post.tags.values_list('id', flat=True)
    # извлекается Python’овский список идентификаторов тегов текущего
    # поста. Набор запросов QuerySet values_list() возвращает кортежи со
    # значениями заданных полей. Ему передается параметр flat=True, чтобы
    # получить одиночные значения, такие как [1, 2, 3, ...], а не одноэлементые кортежи,
    # такие как [(1,), (2,), (3,) ...];
    similar_post = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # берутся все посты, содержащие любой из этих тегов, за исключением
    # текущего поста;
    similar_post = similar_post.annotate(same_tags=Count('tags')).order_by('-same_tags',
                                                                           '-publish')[:4]
    #  применяется функция агрегирования Count. Ее работа – генерировать
    # вычисляемое поле – same_tags, – которое содержит число тегов, общих
    # со всеми запрошенными тегами;
    # результат упорядочивается по числу общих тегов (в  убывающем порядке) и  по publish, чтобы сначала отображать последние посты для
    # постов с одинаковым числом общих тегов. Результат нарезается, чтобы
    # получить только первые четыре поста;
    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'form': form,
                                                     'comments': comments,
                                                     'similar_posts': similar_post})


# Мы используем предоставляемый веб-фреймворком Django декоратор
# require_POST, чтобы разрешить запросы методом POST только для этого представления.
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    # Определяется переменная comment с изначальным значением None. Указанная переменная будет использоваться для хранения комментарного
    # объекта при его создании.
    comment = None
    # Комментарий был отправлен
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Создать объект класса Comment, не сохраняя его в базе данных
        comment = form.save(commit=False)
        # Метод save() создает экземпляр модели, к которой форма привязана,
        # и сохраняет его в базе данных. Если вызывать его, используя commit=False,
        # то экземпляр модели создается, но не сохраняется в базе данных. Такой
        # подход позволяет видоизменять объект перед его окончательным сохранением.
        # Назначить пост комментарию
        comment.post = post
        # Пост назначается созданному комментарию: comment.post = post
        # Сохранить комментарий в базе данных
        comment.save()
    return render(request, "blog/post/comment.html", {'post': post,
                                                      'form': form,
                                                      'comment': comment})