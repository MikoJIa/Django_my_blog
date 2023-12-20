import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post

#  создание новостных лент для постов
class LatestPostsFeed(Feed):
    title = 'My blog'
    link = reverse_lazy('blog:post_list')
    #  Функция-утилита reverse_lazy() используется для того, чтобы генерировать
    #  URL-адрес для атрибута link. Метод reverse() позволяет формировать
    # URL-адреса по их имени и передавать опциональные параметры. Мы использовали
    # reverse() в главе 2 «Усовершенствование блога за счет продвинутых
    # функциональностей»
    description = 'New post of my blog.'

    def items(self):
        return Post.published.all()[:5]
    #  Метод items() извлекает включаемые в новостную ленту объекты.
    #  Мы извлекаем последние пять опубликованных постов, которые затем будут
    #  включены в новостную ленту.

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30)
    # В методе item_description() используется функция markdown() ,
    # чтобы конвертировать контент в формате Markdown в формат HTML,
    # и функция шаблонного фильтра truncatewords_html(), чтобы сокращать описание постов
    # после 30 слов, избегая незакрытых HTML-тегов.

    def item_pubdate(self, item):
        return item.publish

