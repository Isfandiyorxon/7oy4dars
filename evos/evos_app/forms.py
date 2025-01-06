from .models import Dish,Category,Coments
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class OvqatFrom(forms.Form):

    name=forms.CharField(max_length=150,widget=forms.TextInput(attrs={
        "placeholder": "Ovqat nomi",
        'class': "form-control"
    }))

    about=forms.CharField(max_length=150,widget=forms.Textarea(attrs={
        "placeholder": "Ovqat haqida",
        'class': "form-control",
        'rows':3
    }))
    photo=forms.ImageField(required=False,widget=forms.FileInput())
    category=forms.ModelChoiceField(queryset=Category.objects.all(),
                               widget=forms.Select(attrs={
                                   'class': 'form-select'

                               }))


    # def __init__(self,request,data=None, files=None,initial=None):
    #     super().__init__(data=data, files=files , initial=initial)
    #     if not request.user.is_superuser and 'update'  not in request.path:
    #         self.chef = forms.ModelChoiceField(queryset=User.objects.all(),
    #                                       widget=forms.Select())
    def create(self,request):
        dish=Dish.objects.create(**self.cleaned_data)
        dish.chef = request.user
        dish.save()
        return dish

def validate_username(username):
    if " " in username:
        raise ValidationError("use nameda bo'sh joy bo'lishu mumkin emans")

class RegistrationForm(forms.Form):
    username=forms.CharField(max_length=150,error_messages={"error":"max 150 ta belgi bo'lishi kerak"},
                             widget=forms.TextInput(attrs={
                                 'id':'form3Example1cg',
                                 "class": "form-control form-control-lg"
                             }),validators=[validate_username])
    email=forms.EmailField(widget=forms.EmailInput(attrs={
        "id": "form3Example3cg",
        "class": "form-control form-control-lg"
    }))
    password=forms.CharField(min_length=4,widget=forms.PasswordInput(attrs={
        "id": "form3Example4cg",
        "class": "form-control form-control-lg"
    }))

    password_repeat=forms.CharField(min_length=4,widget=forms.PasswordInput(attrs={
        "id": "form3Example4cdg",
        "class": "form-control form-control-lg"
    }))
    def clean(self):
        clean_data=super().clean()
        password=clean_data.get("password")
        password_repeat=clean_data.get("password_repeat")
        if not password and not password_repeat or password_repeat != password:
            return  ValidationError("Parollar bir biriga teng bo'lishi kerak")
        return clean_data
class LoginForm(forms.Form):
    username=forms.CharField(max_length=150,widget=forms.TextInput())
    password=forms.CharField(max_length=4,widget=forms.PasswordInput())


class ComentForm(forms.ModelForm):
    class Meta:
        model=Coments
        fields=['text']

class MyEmailForm(forms.Form):
    subject=forms.CharField(max_length=150,widget=forms.TextInput(attrs={
        "class":"form-control"
    }))
    message=forms.CharField(max_length=1000,widget=forms.Textarea(attrs={
        "class": "form-control",
        "maxlength":"1000",
        "rows":"4"

    }))