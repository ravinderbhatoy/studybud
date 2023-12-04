from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Q
from .forms import RoomForm, UserForm, MyUserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Room, Topic, Message, User

# Create your views here.

# rooms = [
#     {"id": 1, "name": "Lets learn python!"},
#     {"id": 2, "name": "Run java together!"},
#     {"id": 3, "name": "Make awesome websites with me!"}
# ]


def login_page(response):
    if response.user.is_authenticated:
        return redirect("home")
    if response.method == "POST":
        email = response.POST.get("email").lower()
        password = response.POST.get("password")
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(response, "User doesn't exist")
        user = authenticate(response, email=email, password=password)
        if user is not None:
            login(response, user)
            return redirect("home")
        else:
            messages.error(response, "Username or Password doesn't exist")
    return render(response, "base/login.html")


def register_page(response):
    form = MyUserCreationForm()
    if response.method == "POST":
        form = MyUserCreationForm(response.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(response, user)
            return redirect("home")
        else:
            messages.error(response, "An error occurred during registration")
    return render(response, "base/register.html", {'form': form})


def logout_user(response):
    logout(response)
    return redirect("home")

def update_user(response):
    user = response.user
    form = UserForm(instance=user)
    context = {'form': form}
    if response.method == "POST":
        form = UserForm(response.POST, response.FILES, instance=user)
        if form.is_valid():         
            form.save()
            return redirect('profile', pk=user.id)
    return render(response, 'base/update-user.html', context)

def home(response):
    q = response.GET.get("q") if response.GET.get("q") != None else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )
    room_count = rooms.count()
    topics = Topic.objects.all()[:5]
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {"rooms": rooms, "topics": topics, "room_count": room_count, "room_messages": room_messages}
    return render(response, "base/home.html", context)


def room(response, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if response.method == 'POST':
        message = Message.objects.create(
            user = response.user,
            room = room,
            body = response.POST.get('body')
        )
        room.participants.add(response.user)
        return redirect('room', pk=room.id)

    context = {"room": room, "room_messages": room_messages, 'participants': participants}
    return render(response, "base/room.html", context)


@login_required(login_url="/login")
def create_room(response):
    form = RoomForm()
    topics = Topic.objects.all()
    if response.method == "POST":
        topic_name = response.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = response.user,
            topic = topic,
            name = response.POST.get('name'),
            description = response.POST.get('description')
        )
        return redirect('home')

    context = {"form": form, 'topics': topics}
    return render(response, "base/room_form.html", context)


@login_required(login_url="/login")
def update_room(response, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if response.user != room.host:
        return HttpResponse("You are not allwoed here!")
    if response.method == "POST":
        topic_name = response.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = response.POST.get('name')
        room.topic = topic
        room.description = response.POST.get('description')
        room.save()
        return redirect("home")
    context = {"form": form, 'topics': topics, 'room': room}
    return render(response, "base/room_form.html", context)


@login_required(login_url="/login")
def delete_room(response, pk):
    room = Room.objects.get(id=pk)

    if response.user != room.host:
        return HttpResponse("You are not allwoed here!")
    if response.method == "POST":
        room.delete()
        return redirect("home")
    return render(response, "base/delete.html", {"obj": room})

@login_required(login_url="/login")
def delete_message(response, pk):
    message = Message.objects.get(id=pk)
    if response.method == "POST":
        message.delete()
        return redirect("home")
    return render(response, "base/delete.html", {"message": message})

# method to edit user message (optional)

@login_required(login_url="/login")
def edit_message(response, pk):
    message = Message.objects.get(id=pk)
    if response.method == "POST":
        print(response.POST.get('user_message'))
        message.body = response.POST.get('user_message')
        message.save()
        return redirect("home")
    return redirect('room')


def profile_page(response, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()  
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(response, 'base/profile.html', context)

def topics_page(response):
    q = response.GET.get("q") if response.GET.get("q") != None else ""
    topics = Topic.objects.filter(name__icontains=q)
    context = { "topics": topics }
    return render(response, 'base/topics.html', context)

def activity_page(response):
    room_messages = Message.objects.all()
    return render(response, 'base/activity.html', {'room_messages': room_messages})