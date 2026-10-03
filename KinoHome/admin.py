from django.contrib import admin
from .models import Category, Film, Year, Comment, Profile, Gender, Ip

# Register your models here.
admin.site.register(Category)
# admin.site.register(Film)
admin.site.register(Year)
admin.site.register(Ip)


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'duration','release')
    list_display_links = ('id', 'title')


@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = ('id', 'user', 'film', 'created_at',)
    list_display_links = ('id', 'user', 'film')


@admin.register(Profile)
class Profile(admin.ModelAdmin):
    list_display = ('id', 'user', 'gender', 'created_at', 'avatar')
    list_display_links = ('id', 'user')


@admin.register(Gender)
class Gender(admin.ModelAdmin):
    list_display = ('id', 'gender')
    list_display_links = ('id', 'gender')
