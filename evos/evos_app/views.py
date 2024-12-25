from django.shortcuts import render,get_object_or_404,redirect
from .models import Category,Dish
from django.contrib.auth.models import User
from .forms import OvqatFrom,RegistrationForm,LoginForm
from django.contrib.auth import authenticate, login, logout

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
    dish=Dish.objects.filter(category_id=pk)
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

def register(request):
    if request.method == "POST":
        form=RegistrationForm(data=request.POST)
        if form.is_valid():
            password=request.POST["password"]
            password_repeat=request.POST["password_repeat"]
            if password ==password_repeat:
                username=request.POST['username']
                email=request.POST['email']
                user=User.objects.create_user(username,email,password)
                print("Siz ro'yhatdan o'tdingiz!")
                return redirect('login')
    else:
        form=RegistrationForm()

        context={
            'form':form
        }
        return render(request,'auth/register.html',context)

def login_view(request):
    if request.method == 'POST':
        form=LoginForm(data=request.POST)
        if form.is_valid():
            username=request.POST["username"]
            password=request.POST["password"]
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                print("Xush kelibsiz!")
                return redirect('home')
            else:
                print('Username yoki parol hato')
    else:
        form=LoginForm()
    context={
            'form':form
        }
    return render(request,'auth/login.html',context)

def logout_view(request):
    logout(request)
    return redirect('login')