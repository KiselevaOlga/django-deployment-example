from django.urls import path
from first_app import views

app_name = 'first_app'

urlpatterns = [
    path('bob/', views.bob, name='bob'),
    path('searchengines/', views.search_engines, name='search_engine'),
    path('other/', views.other, name='other'),
    path('user_login/', views.user_login, name='user_login'),
]