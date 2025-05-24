from django.urls import path
from .views import *


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('main', hero, name='main'),
    path('', table, name='table'),
    path('create/', create_task, name='create'),
    path('update/<pk>', update_task, name='update'),
    path('mark/<pk>', mark, name='mark'),
    path('unmark/<pk>', unmark, name='unmark'),
    path('delete/<pk>', delete, name='delete'),
    path('forms/', form_create, name='forms'),
    path('register/', register_form, name='register'),
    path('login/', login_form, name='login'),
    path('logout/', logout_form, name='logout'),
]
