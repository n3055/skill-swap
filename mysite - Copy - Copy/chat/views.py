from django.shortcuts import render,HttpResponse,redirect
import random
from .models import rooms
import datetime
def index(request):
    return render(request, "chat/index.html")

def room(request, room_name):
    symbols = ['_','r','Q','F','f','R','q']
    room_id = ""
    r1 = rooms.objects.all()
    for r in r1:
        if r.members < 2:
            room_id = r.room_id
            r.members+=1
            r.save()
            break
        else:
            r.delete()
    if(len(r1)==0 or room_id == ""):
        room_id = str(random.randint(1000,9999))+str(symbols[random.randint(0,6)])
        room_id = room_id + str(symbols[random.randint(0,6)])+str(random.randint(1000,9999))
        r1 = rooms(room_id=room_id,created_at=datetime.datetime.now(),members=1)
        r1.save()
    
    return render(request, "chat/room.html", {"room_name": room_id})
