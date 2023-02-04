from django.shortcuts import render


from .models import Person

def home(request):
    return render(request, 'home.html')

def pic_detail(request, pic_id):
    pic = Person.objects.get(id=pic_id)
    return render(request, 'pic_detail.html', {
        'pic': pic,
    })
