Давай начнем с настройки базовой аутентификации на Django с учетом REST API. Мы создадим REST API для регистрации, входа и выхода пользователей. На этом этапе мы не будем использовать JWT, OAuth или 2FA, а просто настроим базовые API для работы с пользователями. Каждый шаг будет объяснен и протестирован.

Шаг 1: Установка и настройка проекта Django
Создаем проект Django:

bash
    django-admin startproject myproject
    cd myproject
Это создаст основную структуру проекта с настройками, маршрутизацией и базовой конфигурацией.

Создаем приложение для аутентификации пользователей:

bash
    python manage.py startapp accounts
Мы создаем отдельное приложение accounts, которое будет содержать всю логику, связанную с аутентификацией и управлением пользователями. Это приложение облегчит добавление модулей безопасности в будущем.

Добавляем accounts в INSTALLED_APPS в settings.py: Открываем файл settings.py и добавляем accounts в список приложений:

python
    INSTALLED_APPS = [
        ...
        'accounts',
        'rest_framework',  # Подключаем Django REST Framework для API
]
Это позволит Django использовать наше приложение и подключит REST Framework для работы с API.

Шаг 2: Настройка модели пользователя и сериализатора
Используем стандартную модель пользователя Django: Django предоставляет встроенную модель пользователя (User), которая поддерживает базовую регистрацию и вход. Поэтому на этом этапе мы будем использовать её без создания кастомной модели.

Создаем сериализатор для модели пользователя: Сериализатор нужен для преобразования данных модели пользователя в JSON-формат для API. В accounts создаем файл serializers.py и добавляем следующее:

python
    from django.contrib.auth.models import User
    from rest_framework import serializers

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'username', 'email']

Шаг 3: Создаем представления для регистрации, входа и выхода
Создаем представление для регистрации: В accounts/views.py добавляем представление для регистрации нового пользователя. Оно будет принимать username, email, и password, а затем создавать нового пользователя.

python
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from accounts.serializers import UserSerializer

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        # Проверка, что пользователь с таким именем не существует
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем нового пользователя
        user = User.objects.create_user(username=username, email=email, password=password)
        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
Это представление проверяет наличие пользователя с таким же именем, а затем создает нового пользователя, если его нет. Оно возвращает данные нового пользователя в формате JSON.

Создаем представление для входа: Вход требует проверки введенных данных. Создаем это представление также в accounts/views.py:

python
Копировать код
from django.contrib.auth import authenticate, login

@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
Функция authenticate проверяет имя пользователя и пароль. Если данные верны, пользователь авторизуется, и возвращается сообщение об успешном входе.

Создаем представление для выхода: В этом представлении вызываем функцию logout, чтобы завершить сессию пользователя:

python
Копировать код
from django.contrib.auth import logout

@api_view(['POST'])
def logout_user(request):
    logout(request)
    return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
Шаг 4: Настраиваем маршруты для API
Добавляем маршруты API в accounts/urls.py: Создаем файл urls.py в приложении accounts и добавляем маршруты для регистрации, входа и выхода:

python
Копировать код
from django.urls import path
from .views import register_user, login_user, logout_user

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]
Подключаем маршруты API к основному проекту: В файле myproject/urls.py подключаем маршруты из приложения accounts:

python
Копировать код
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),  # Подключаем маршруты для приложения accounts
]

