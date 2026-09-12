from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('ads:home')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            next_url = 'analytics:dashboard' if user.is_staff else 'ads:home'
            return redirect(request.GET.get('next', next_url))
        else:
            messages.error(request, 'Неверный логин или пароль.')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из аккаунта.')
    return redirect('ads:home')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('ads:home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна! Добро пожаловать!')
            return redirect('ads:home')
        else:
            messages.error(request, 'Ошибка при регистрации. Проверьте данные.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


def is_superuser_check(user):
    return user.is_authenticated and user.is_superuser


@user_passes_test(is_superuser_check, login_url='accounts:login')
def manage_users(request):
    users = User.objects.all().order_by('-date_joined')

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        target_user = get_object_or_404(User, pk=user_id)

        if target_user == request.user:
            messages.error(request, 'Вы не можете изменять свои права.')
            return redirect('accounts:manage_users')

        if action == 'make_admin':
            target_user.is_staff = True
            target_user.is_superuser = True
            target_user.save()
            messages.success(request, f'{target_user.username} теперь администратор.')

        elif action == 'make_staff':
            target_user.is_staff = True
            target_user.is_superuser = False
            target_user.save()
            messages.success(request, f'{target_user.username} теперь персонал.')

        elif action == 'make_user':
            target_user.is_staff = False
            target_user.is_superuser = False
            target_user.save()
            messages.success(request, f'{target_user.username} теперь обычный пользователь.')

        elif action == 'deactivate':
            target_user.is_active = False
            target_user.save()
            messages.success(request, f'{target_user.username} деактивирован.')

        elif action == 'activate':
            target_user.is_active = True
            target_user.save()
            messages.success(request, f'{target_user.username} активирован.')

        elif action == 'delete':
            target_user.delete()
            messages.success(request, 'Пользователь удалён.')

        return redirect('accounts:manage_users')

    context = {'users': users}
    return render(request, 'accounts/manage_users.html', context)