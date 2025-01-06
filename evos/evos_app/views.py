from django.contrib.auth.decorators import permission_required,login_required

from django.contrib.messages.context_processors import messages
from django.shortcuts import render,get_object_or_404,redirect
from django.core.handlers.wsgi import WSGIRequest

from .models import Category,Dish,Coments,MyUser
from .forms import OvqatFrom,RegistrationForm,LoginForm,ComentForm,MyEmailForm
from django.contrib.auth import authenticate, login, logout

from django.core.mail import send_mail

from django.conf import settings

from django.db.models import Q

# Create your views here.

def home(request ):
    category=Category.objects.all()
    dish=Dish.objects.all()
    context={
        'category':category,
        'dish':dish
    }
    return render(request,'home.html',context)
@login_required(login_url='login')
def dish_detaling(request,pk):
    dish=get_object_or_404(Dish,pk=pk)
    category=Category.objects.all()
    context={
        'dish':dish,
        'category':category,
        'comment_form':ComentForm,
        'commnets':Coments.objects.filter(dish_id=pk)
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
@permission_required('evos_app.add_dish','home')
def add_dish(request):
    if request.method == 'POST':
        form=OvqatFrom(data=request.POST,files=request.FILES)
        if form.is_valid():
            dish=form.create(request)
            messages.success(request,f"{dish.name} qo'shildi")
            return redirect('dish_detaling',pk=dish.pk)
        else:
            print(form.errors)
    else:
        form=OvqatFrom()
        context={
            'form':form
        }
        return render(request,'add_dish.html',context)
@permission_required('evos_app.change_dish','home')
def update_dish(request,pk):
    dish=get_object_or_404(Dish,pk=pk)
    if dish.chef == request.user or request.user.is_superuser:
        if request.method=='POST':
            form=OvqatFrom(request,data=request.POST,files=request.FILES)
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
    else:
        messages.error(request,"sizda bundeay huquq yo'q😒😒😒😒")
@permission_required('evos_app.delete_dish','home')

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
                user=MyUser.objects.create_user(username,email,password)
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

def comment_save(request,dish_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            form=ComentForm(data=request.POST)
            if form.is_valid():
                comment=Coments.objects.create(
                    text=form.cleaned_data.get('text'),
                    user=form.cleaned_data.get('user'),
                    dish=get_object_or_404(Dish,pk=dish_id)
                )
                #messages.success(request,"Comment qo'shildi")
        return redirect('dish_detaling',pk=dish_id)
    else:
       # messages.error(request, "Avval ro'yxatdan o'ting")
        return redirect('login')

def delete_comment(request,comment_id,dish_id):
    commnet=get_object_or_404(Coments,pk=comment_id)
    if commnet.user == request.user or request.user.is_superuser:
        commnet.delate()
        messages.success(request,"Comment o'chirildi!!!")
    return redirect('dish_detaling',pk=dish_id)

def send_message_email(request:WSGIRequest):
    if request.user.is_staff:
        if request.method == 'POST':
            form =MyEmailForm(data=request.POST)
            if form.is_valid():
                for user in MyUser.objects.all():
                    send_mail(
                        form.cleaned_data.get('subject'),
                        form.cleaned_data.get('message'),
                        settings.EMAIL_HOST_USER,
                        [user.email]

                    )
        context={
            "form":MyEmailForm()
        }
        return render(request,'send_email.html',context)
    else:
        messages.error(request,"sizga mumkin emas 😒😒😒")
        return redirect('home')

def search_view(request:WSGIRequest):
    if request.GET.get('word',False):
        word=request.GET.get('word')
        dish=Dish.objects.filter(Q(name__icontains=word)|Q(dish__icontains=word))
        context={
            "dish":dish
        }
        return render(request,'home.html',context)
