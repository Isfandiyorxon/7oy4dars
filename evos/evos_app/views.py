from django.shortcuts import render,get_object_or_404,redirect
from .models import Category,Dish
from .forms import OvqatFrom
# Create your views here.

def home(request ):
    category=Category.objects.all()
    dish=Dish.objects.all()
    context={
        'category':category,
        'dish':dish
    }
    return render(request,'home.html',context)

def dish_detaling(request,pk):
    dish=get_object_or_404(Dish,pk=pk)
    category=Category.objects.all()
    context={
        'dish':dish,
        'category':category
    }
    return render(request,'index.html',context)
def dish_to_category(request,pk):
    dish=Dish.objects.filter(pk=pk)
    category =Category.objects.all()
    context={
        'dish':dish,
        'category':category
    }
    return render(request,'home.html',context)
def add_dish(request):
    if request.method == 'POST':
        form=OvqatFrom(data=request.POST,files=request.FILES)
        if form.is_valid():
            dish=form.create()
            return redirect('dish_detaling',pk=dish.pk)
        else:
            print(form.errors)
    else:
        form=OvqatFrom()
        context={
            'form':form
        }
        return render(request,'add_dish.html',context)

def update_dish(request,pk):
    dish=get_object_or_404(Dish,pk=pk)
    if request.method=='POST':
        form=OvqatFrom(data=request.POST,files=request.FILES)
        if form.is_valid():
            dish.name=form.cleaned_data.get("name")
            dish.about=form.cleaned_data.get("about")
            dish.photo=form.cleaned_data.get("photo")if form.cleaned_data.get("photo") else dish.photo
            dish.category=form.cleaned_data["category"]
            dish.save()
            return redirect('dish_detaling',pk=dish.pk)
    form=OvqatFrom(initial={
        "name":dish.name,
        'about':dish.about,
        'photo':dish.photo,
        "category":dish.category
    })

    context={
        'form':form,
        'dish':dish
    }

    return render(request,'add_dish.html',context)

def delate_dish(request,pk):
    dish=get_object_or_404(Dish,pk=pk)
    if request.method == 'POST':
        dish.delete()
        return redirect('home')

    context={
        'dish':dish
    }
    return render(request,'delete_dish.html',context)