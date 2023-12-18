from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    # Давайте создадим конкретно-прикладной менеджер, чтобы извлекать все
    # посты, имеющие статус PUBLISHED.
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        # Мы определили перечисляемый класс Status путем подклассирования
        # класса models.TextChoices. Доступными вариантами статуса поста являются
        # DRAFT и PUBLISHED. Их соответствующими значениями выступают DF и PB, а их
        # метками или читаемыми именами являются Draft и Published.


    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')  # поле слаг будет уникальным для даты publish
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices,
                              default=Status.DRAFT)

    objects = models.Manager()  # менеджер, применяемый по умолчанию
    published = PublishedManager()  # конкретно-прикладной менеджер
    tags = TaggableManager()  # Менеджер tags позволит добавлять, извлекать и удалять теги из объектов
    # Post.


    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    # Функция reverse() будет формировать URL-адрес динамически, применяя
    # имя URL-адреса, определенное в шаблонах URL-адресов.
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.month,
                                                 self.publish.day,
                                                 self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # Атрибут related_name позволяет назначать имя атрибуту,
    # который используется для связи от ассоциированного объекта назад к нему.
    # Пост комментарного объекта можно извлекать посредством comment.post и все комментарии,
    # ассоциированные с  объектом-постом, – посредством post.comment.all()
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
