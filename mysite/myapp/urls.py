from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.index),
    path('contacts/', views.contacts),
    path('about/', views.about)
]
