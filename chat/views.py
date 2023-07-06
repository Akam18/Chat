from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from chat.models import Message
from django.shortcuts import render, redirect

from .models import Message
from .serializers import MessageSerializer, UserSerializer

# Create your views here.


def IndexView(request):
    if request.user.is_authenticated():
        return redirect('chat')
    
    if request.method == 'GET':
        return render(request, 'index.html', {})
    
    if request.method == 'POST':
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username= username, password= password)

        if user is not None:
            login(request, user)
            return
        else:
            return HttpResponse('{"error": "User does not exist"}')    

def LogoutView(request):
    logout(request)
    return redirect('/')

@csrf_exempt    # не надо создавать ццрф для 
def message_list(request, sender=None, receiver=None):
    if request.method == 'GET':
        message = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(message, many=True, context={'request': request})
        for message in message:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer= MessageSerializer(data= data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)  # 201 - 
        return JsonResponse(serializer.errors, status=400)  # 400 - ваш запрос не прошел
    

def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if request.method == "GET":
        usernames = {
            "user": User.objects.exclude(username=request.user.username)
                    }
        return render(request, "chat.html", context=usernames)
    

def message_view(request, sender, receiver):
    if not request.user.is_authenticated:
        return redirect('/')

    if request.method == "GET":

        info ={
            "users": User.objects.exclude(username=request.user.username), #  exclude отображает все кроме самого себя
            "receivers": User.objects.get(id= receiver),
            "message": Message.objects.filter(sender_id=sender, receiver_id= receiver) |
            Message.objects.filter(sender_id=receiver, receiver_id= sender),
            }
        return render(request, "messages.html", context=info)        





