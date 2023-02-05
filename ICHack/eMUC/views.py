from django.shortcuts import render
from django.http import Http404
from .models import Person
from .terra import main

from .models import Picture

def home(request):
    return render(request, 'home.html')

def pic_detail(request, pic_id):
    try:
        pic = Picture.objects.filter(pk=pic_id).values()
        # print("sdfg",pic)
    except:
        return Http404('pic not found')
    return render(request, 'pic_detail.html', {
        'pic': pic,
    })

def start(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        sex = request.POST.get('sex')
        emotion = main.get_emotion()

        person = Person(name=name, age=age, sex=sex)
        person.save()
        #redirect('success')

    return render(request, 'start.html', {"emotion":emotion})