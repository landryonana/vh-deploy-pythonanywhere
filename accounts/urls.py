from django.urls import path
from django.contrib.auth import views as auth_views

from accounts import views



app_name = "accounts"

urlpatterns = [
    path('login/', views.user_login, name="user_login"),
    path('logout/', views.user_logout, name="user_logout"),
    path('param/', views.param, name="param"),

    path('mot-de-passe-change/', views.change_password, name='password_change'),
    path('mot-de-passe-change/reussi/', views.password_change_done, name='password_change_done'),

    #====================AJAX LEAVE
    path('register/', views.user_register, name="user_register"),
    path('edit-user/', views.user_edit, name="user_edit"),
    path('users/', views.users, name="users"),
    path('user/<int:pk>/supprimer', views.user_delete, name="user_delete"),
    path('user/<int:pk>/detail', views.user_detail, name="user_detail"),
]
