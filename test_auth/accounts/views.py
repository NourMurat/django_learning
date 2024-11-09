from django.shortcuts import render

# домашняя страница
from django.http import HttpResponse

def home_page(request):
    return render(request, 'accounts/homepage.html')

def login_page(request):
    return render(request, 'accounts/login.html')

def register_page(request):
    return render(request, 'accounts/register.html')

def about_game(request):
    return render(request, 'accounts/aboutGame.html') 

# ========================== AUTHENTIFICATION ==============================

# Создаем представление для РЕГИСТРАЦИИ:
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
# from accounts.serializers import UserSerializer
from django.shortcuts import redirect

# Это представление проверяет наличие пользователя с таким же именем, 
# а затем создает нового пользователя, если его нет. 
# Оно возвращает данные нового пользователя в формате JSON.
@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        # Получение данных из request.POST
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        password_confirm = request.POST.get('password2')

        # Проверка на наличие username и password
        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Проверка, что пользователь с таким именем не существует
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Проверка совпадения паролей
        if password != password_confirm:
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        # Создание нового пользователя
        user = User.objects.create_user(username=username, email=email, password=password)
        # serializer = UserSerializer(user)
        # return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Перенаправляем на страницу входа после успешной регистрации
        return redirect('login')  # Здесь используется имя URL для страницы входа

# Создаем представление для ВХОДА:
from django.contrib.auth import authenticate, login

# Вход требует проверки введенных данных
# Функция authenticate проверяет имя пользователя и пароль. Если данные верны, 
# пользователь авторизуется, и возвращается сообщение об успешном входе.
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


# Создаем представление для ВЫХОДА:
from django.contrib.auth import logout

# В этом представлении вызываем функцию logout, чтобы завершить сессию пользователя
@api_view(['POST'])
def logout_user(request):
    logout(request)
    return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


