from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from .models import User, Message
from django.db.models import Q
import json
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate,login as loginuser,logout,get_user_model
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def chatroom(request, pk):
    other_user = get_object_or_404(User,username=pk)
    messages = Message.objects.filter(
        Q(receiver=request.user, sender=other_user)
    )
    users = User.objects.all()
    messages.update(seen=True)
    messages = messages | Message.objects.filter(Q(receiver=other_user, sender=request.user))
    return render(request, "chatroom.html", {"other_user": other_user, "messages": messages,'users':users})


@login_required(login_url='login')
def ajax_load_messages(request, pk):
    other_user = get_object_or_404(User,pk=pk)
    #other_user=User.objects.get(id=pk)
    messages = Message.objects.filter(seen=False).filter(
        Q(receiver=request.user, sender=other_user)
    )
    message_list = [{
        "sender": message.sender.username,
        "message": message.message,
        "sent": message.sender == request.user
    } for message in messages]
    messages.update(seen=True)

    if request.method == "POST":
        message = json.loads(request.body)
        m = Message.objects.create(receiver=other_user, sender=request.user, message=message)
        message_list.append({
            "sender": request.user.username,
            "message": m.message,
            "sent": True,
        })
    print(message_list)
    return JsonResponse(message_list, safe=False)



def login(request):
    if request.method == 'POST':
        print("hi")
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print("done",user)
            if user is not None:
                loginuser(request,user)
                return redirect('home')
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})
def signup(request):
    if request.method=='POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})
@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        User = get_user_model()
        users=User.objects.all()
        print(users)
        return render(request , 'index.html' , context={'users' : users})
def signout(request):
    logout(request)
    return redirect('login')