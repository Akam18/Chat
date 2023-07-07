from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView, name= 'index'),
    path('chat/', views.chat_view, name= 'chats'),
    path('chat/<int:sender>/<int:receiver>/', views.message_view, name='chat'),
    path('api/message/<int:sender>/<int:receiver>/', views.message_list, name= 'message_detail'),
    path('api/messages/', views.message_list, name='logout'),
    path('logout/', views.LogoutView, name='logout'),
    path('register/', views.register_view, name='register'),

         
]