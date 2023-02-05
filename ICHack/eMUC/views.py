from django.shortcuts import render,redirect
from django.http import Http404
from .models import Person
import random


from .models import Picture

def home(request):
    return render(request, 'home.html')

def pic_detail(request, pic_id):
   count = 0
    persons = []
    """ while (count < 11):
        number = random.randint(1,1113)
        person = Person.objects.get(id=number)
        persons.append(person)
        count = count + 1 """
    return render(request, 'pic_detail.html', {
        'persons': persons,
    })

def start(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        sex = request.POST.get('sex')

        person = Person(name=name, age=age, sex=sex)
        person.save()
        #redirect('success')

    return render(request, 'start.html')
