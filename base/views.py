from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Room,Topic,Message,User

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from django.contrib import messages
from .forms import RoomForm,UserForm,MyUserCreationForm
# Create your views here.

# rooms =[
#     {'id':1,'name':'lets learn python'},
#     {'id':2,'name':'design with me'},
#     {'id':3,'name':'front end developer'},
# ]

def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('/')
    if request.method=="POST":
        username=request.POST.get("username").lower()
        password=request.POST.get("password")

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request, 'NO SUCH USER')

        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
             messages.error(request, 'username or password is invalid')


    context={'page':page}
    return render(request,'base/login_register.html',context)
def logoutPage(request):
    logout(request)
    return redirect('/login/')

def registerPage(request):
    page='register'
    form=MyUserCreationForm()
    if request.method=="POST":
        form=MyUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('/')
        else:
            messages.error(request,'An error occured during register')

    context={'page':page,'form':form}
    
    return render(request,'base/login_register.html',context)




def home(request):
    q=request.GET.get("q") if request.GET.get("q")!=None else ''


    rooms=Room.objects.filter(Q(topic__name__icontains=q)|
                              Q(name__icontains=q)|
                              Q(description__icontains=q))
    topics=Topic.objects.all()[0:3]
    room_message=Message.objects.filter(Q(room__topic__name__icontains=q)|
                              Q(room__name__icontains=q)|
                              Q(room__description__icontains=q))
    room_count=rooms.count()
    context={'text':"homeview",'rooms':rooms,'topics':topics,'room_count':room_count,'room_message':room_message}
    return render(request,'base/home.html',context)

def room(request,pk):
    room=Room.objects.get(id=pk)
    room_message=Message.objects.filter(room=room).order_by('-created')
    if request.method=='POST':
        if request.POST.get('body')==None:
            print('IT iS NONE')
        print('message',request.POST.get('body'),pk)
     #and request.POST.get('body')!=None:
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')

        )
        message.save()
        id=pk
        room1='room'
        room.participant.add(request.user)
        return redirect(f'/room/{pk}')
    
    participants=room.participant.all()
    context={'text':"room",
     'room':room,
     'room_message':room_message,
     'participants':participants
    }
    
    return render(request,"base/room.html",context)


@login_required(login_url='/login')
def createRoom(request):
    form =RoomForm()
    topics=Topic.objects.all()
    context={'form':form,'topics':topics}



    if request.method=="POST":
        topic_name=request.POST.get("topic")
        topic, created=Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
           host=request.user,
           topic=topic,
           name=request.POST.get('name'),
           description=request.POST.get('description'),)
        return redirect('/')
        # form=RoomForm(request.POST)
        # if form.is_valid():
        #     room=form.save(commit=False)
        #     room.host=request.user
        #     room.participant=request.user
        #     room.save()
        

    return render(request,"base/room_form.html",context)
@login_required(login_url='/login')
def updateRoom(request,pk):
    
    room =Room.objects.get(id=pk)
    form =RoomForm(instance=room)
    context={'form':form,'room':room}
    if request.user!=room.host:
        return HttpResponse("You Dont Belong here")

    if request.method=="POST":
        topic_name=request.POST.get("topic")
        topic, created=Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic=topic
        room.description=request.POST.get('description')
        room.save()
        return redirect('/')
        
        # form=RoomForm(request.POST,instance=room)
        # if form.is_valid():
        #     form.save()
            
    
    return render(request,'base/room_form.html',context)
@login_required(login_url='/login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user!=room.host:
        return HttpResponse("You Dont Belong here")
    if request.method=="POST":
        room.delete()
        return redirect('/')

    return render(request,'base/delete.html',{})


def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    room_message=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,'room_message':room_message,'topics':topics,'rooms':rooms}

    return render(request,'base/profile.html',context)

@login_required(login_url='/login')
def updateUser(request):
    user=request.user
    form=UserForm(instance=user)
    if request.method=='POST':
        form= UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()   
                   
            return redirect(f'/user-profile/{user.id}')

    context={'form':form}
    return render(request,'base/update-user.html',context)


def topicPage(request):
    q=request.GET.get("q") if request.GET.get("q")!=None else ''
    topics=Topic.objects.filter(name__icontains=q)
    context={'topics':topics}
    return render(request,'base/topics.html',context)


def activityPage(request):
    room_messages=Message.objects.all()
    context={'room_messages':room_messages}
    return render(request,'base/activity.html',context)
