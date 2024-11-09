from django.urls import path
from .views import (
    home_page,
    login_page,
    register_page,
    about_game,
    register_user,
    login_user,
    logout_user,
)

urlpatterns = [
    # Пути для отображения HTML-страниц
    path('', home_page, name='home'),  # Главная страница
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('about_game/', about_game, name='about_game'),  # Пример маршрута для AboutGame
    path('logout/', logout_user, name='logout'),  # Маршрут для logout

    # Пути для API-запросов с префиксом 'api/'
    path('api/register/', register_user, name='api_register'),
    path('api/login/', login_user, name='api_login'),
    path('api/logout/', logout_user, name='api_logout'),
]
