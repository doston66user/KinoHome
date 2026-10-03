from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.templatetags.static import static
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=40, verbose_name='Название категории')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'


class Year(models.Model):
    title = models.CharField(max_length=15, verbose_name='Года выпуска')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('years', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Год выпуска'
        verbose_name_plural = 'Года выпуска'


class Film(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название Каталога(Фильма/Мультфильма/Сериала)')
    description = models.TextField(verbose_name='Описание Каталога(Фильма/Мультфильма/Сериала)')
    image = models.ImageField(upload_to='film_preview/', verbose_name='Картина')
    movie = models.FileField(upload_to='videos/', null=True, blank=True,
                             verbose_name='Видео фильма')  # null=True, blank=True, Я написал потому что у меня нет файлов с фильмами я их ещё не скачал
    trailer = models.FileField(upload_to='trailers/', null=True, blank=True, verbose_name='Трейлер')
    release = models.ForeignKey(Year, on_delete=models.CASCADE, verbose_name='Дата выпуска')
    country = models.CharField(max_length=40, verbose_name='Страна')
    genre = models.ManyToManyField(Category, verbose_name='Жанр', related_name='films')
    duration = models.CharField(max_length=20, verbose_name='Продолжительность')
    premier = models.CharField(max_length=50, verbose_name='Премьера (РФ)')
    director = models.CharField(max_length=50, verbose_name='Режиссер')
    cast = models.CharField(max_length=200, verbose_name='Актеры')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания ')
    views = models.ManyToManyField('Ip', verbose_name='Просмотры', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('film', kwargs={'pk': self.pk})

    def count_views(self):
        if self.views:
            return self.views.count()
        else:
            return 0

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class Comment(models.Model):
    text = models.TextField(max_length=500, verbose_name='Тект Комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания ')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, verbose_name='Фильм')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f'Коментарий пользователя {self.user.username} к фильму {self.film.title} : '

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Gender(models.Model):
    gender = models.CharField(max_length=30, unique=True, verbose_name='Пол')

    def __str__(self):
        return self.gender

    class Meta:
        verbose_name = 'Пол'
        verbose_name_plural = 'Пола'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    avatar = models.ImageField(upload_to='profiles/', verbose_name='Аватар профиля', null=True, blank=True)
    about = models.CharField(max_length=200, verbose_name='О себе', default='Я не хочу указывать никакую информацию о себе')
    phone = models.CharField(max_length=40, verbose_name='Номер Телефона', default='+(012) 345 67 89')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    email = models.EmailField(verbose_name='Почта', null=True, blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, verbose_name='Пол')
    country = models.CharField(max_length=64, verbose_name='Страна/Регион', default='Узбекистан')

    def __str__(self):
        return f'Профиль пользователя {self.user.username}'

    @property
    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        if self.gender and self.gender.gender.strip().lower() == 'мужской':
            return static('kino_static/images/male.png')
        elif self.gender and self.gender.gender.strip().lower() == 'женский':
            return static('kino_static/images/femail.png')
        else:
            return static('kino_static/images/donotknow.jpeg')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'



class Ip(models.Model):
    ip = models.CharField(max_length=50, verbose_name='Апи Пользователя')

    def __str__(self):
        return f'Ip:{self.ip}'

    class Meta:
        verbose_name = 'Ip пользователя'
        verbose_name_plural = 'Ip Пользователей'
