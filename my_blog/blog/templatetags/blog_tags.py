from django import template
from django.db.models import Count

from ..models import Post

register = template.Library()


@register.simple_tag
def total_post():
    return Post.published.count()
# Мы создали простой шаблонный тег, который возвращает количество опубликованных в блоге постов
# Для того что бы быть допустимой библиотекой тегов, в каждом содержащем
# шаблонные теги модуле должна быть определена переменная с именем register
# Эта переменная является экземпляром класса template.Library, и она
# используется для регистрации шаблонных тегов и фильтров приложения.


# Мы создадим еще один тег, чтобы отображать последние посты на боковой
# панели блога.
@register.inclusion_tag('blog/post/latest_posts.html')
# В приведенном выше исходном коде мы зарегистрировали шаблонный
# тег, применяя декоратор @register.inclusion_tag.
def show_latest_posts(count=5):
    #  Данная переменная используется для
    # того, чтобы ограничивать результаты запроса Post.published.order_by('-pub lish')[:count].
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


# Наконец, мы создадим простой шаблонный тег, который возвращает значение.
# Мы сохраним результат в реиспользуемой переменной, не выводя его
# напрямую. Мы создадим тег, чтобы отображать посты с наибольшим числом
# комментариев.
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

#  В приведенном выше шаблонном теге с помощью функции annotate() формируется набор
#  запросов QuerySet, чтобы агрегировать общее число комментариев к каждому посту.