from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Category, Year, Film, Comment, Profile, Gender, Ip
from django.contrib.auth import login, logout, update_session_auth_hash
from .forms import LoginForm, RegisterForm, CommentForm, EditAccountForm, EditProfileForm
from django.views.generic import UpdateView
from django.urls import reverse
from .tests import get_user_ip


def main_page(request):
    years = Year.objects.all()
    films = Film.objects.all().order_by('-created_at')
    latest_films = Film.objects.order_by('-created_at')[:6]
    latest_comments = Comment.objects.order_by('-created_at')[:8]
    categories = Category.objects.all()

    context = {
        'years': years,
        'categories': categories,
        'films': films,
        'latest_films': latest_films,
        'latest_comments': latest_comments,
        'title': 'KinoHome смотри и наслаждайся'
    }
    return render(request, 'KinoHome/main.html', context)


def film_by_category_year(request, pk):
    films = Film.objects.filter(genre__pk=pk).order_by('-created_at')
    genre = Category.objects.get(pk=pk)
    years = Year.objects.all()
    latest_films = Film.objects.order_by('-created_at')[:6]
    latest_comments = Comment.objects.order_by('-created_at')[:8]
    categories = Category.objects.all()

    context = {
        'films': films,
        'years': years,
        'latest_films': latest_films,
        'categories': categories,
        'latest_comments': latest_comments,
        'title': f'Фильмы жанр: {genre.title}'
    }
    return render(request, 'KinoHome/main.html', context)


def film_by_year(request, pk):
    films = Film.objects.filter(release=pk).order_by('-created_at')
    year = Year.objects.get(pk=pk)
    years = Year.objects.all()
    latest_films = Film.objects.order_by('-created_at')[:6]
    latest_comments = Comment.objects.order_by('-created_at')[:8]
    categories = Category.objects.all()

    context = {
        'films': films,
        'years': years,
        'latest_films': latest_films,
        'categories': categories,
        'latest_comments': latest_comments,
        'title': f'Фильмы год: {year.title}'
    }
    return render(request, 'KinoHome/main.html', context)


def film_detail(request, pk):
    film = Film.objects.get(pk=pk)
    ip = get_user_ip(request)

    ip_obj, _ = Ip.objects.get_or_create(ip=ip)

    if not film.views.filter(pk=ip_obj.pk).exists():
        film.views.add(ip_obj)

    years = Year.objects.all()
    latest_films = Film.objects.order_by('-created_at')[:6]
    categories = Category.objects.all()
    latest_comments = Comment.objects.order_by('-created_at')[:8]
    genres = film.genre.all()
    same_films = Film.objects.filter(genre__in=genres).exclude(pk=film.pk)[:4]

    context = {
        'title': f'Фильм {film.title}',
        'film': film,
        'years': years,
        'latest_films': latest_films,
        'categories': categories,
        'comments': Comment.objects.filter(film=film),
        'latest_comments': latest_comments,
        'same_films': same_films,
    }

    if request.user.is_authenticated:
        context['comment_form'] = CommentForm()

        print('IP:', ip)

    return render(request, 'KinoHome/film_detail.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:
        if request.method == 'POST':
            form = LoginForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                if user:
                    login(request, user)
                    return redirect('main')
        else:
            form = LoginForm()

        context = {
            'title': 'Войти в аккаунт',
            'form': form
        }
        return render(request, 'KinoHome/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('main')


def about_page(request):
    context = {
        'title': 'О сайте KinoHome'
    }
    return render(request, 'KinoHome/about_us.html', context)


def register_user(request):
    if request.user.is_authenticated:
        return redirect('main')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            gender = form.cleaned_data['gender']
            profile = Profile.objects.create(user=user, gender=gender)
            profile.save()
            return redirect('login')
    else:
        form = RegisterForm()

    context = {
        'title': 'Регистрация',
        'form': form
    }
    return render(request, 'KinoHome/register.html', context)


def save_comment(request, pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.film = Film.objects.get(pk=pk),
                comment.save()

    return redirect('film', pk)


class CommentUpdate(UpdateView):
    form_class = CommentForm
    model = Comment

    def get_success_url(self):
        comment = Comment.objects.get(pk=self.kwargs['pk'])
        return reverse('film', kwargs={'pk': comment.film.pk})


def delete_comment(request, pk, film_pk):
    user = request.user if request.user.is_authenticated else None
    if user:
        try:
            comment = Comment.objects.get(pk=pk, user=user)
            comment.delete()
        except:
            pass

    return redirect('film', film_pk)


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    default_gender, _ = Gender.objects.get_or_create(gender__iexact='Я не желаю указывать',
                                                     defaults={'gender': 'Я не желаю указывать'})

    profile, _ = Profile.objects.get_or_create(
        user=request.user,
        defaults={'gender': default_gender}
    )

    context = {
        'title': f'Профиль {profile.user.username}',
        'profile': profile,
        'account_form': EditAccountForm(instance=request.user),
        'profile_form': EditProfileForm(instance=profile)
    }

    return render(request, 'KinoHome/profile.html', context)


def edit_account_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            account_form = EditAccountForm(request.POST, instance=request.user)
            profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if account_form.is_valid() and profile_form.is_valid():
                account_form.save()
                profile_form.save()

                data = account_form.cleaned_data
                user = User.objects.get(id=request.user.id)
                if user.check_password(data['old_password']):
                    if data['old_password'] and data['new_password'] == data['confirm_password']:
                        user.set_password(data['new_password'])
                        user.save()
                        update_session_auth_hash(request, user)

                return redirect('profile')
