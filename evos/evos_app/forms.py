from .models import Dish,Category
from django import forms

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
    def create(self):
        dish=Dish.objects.create(**self.cleaned_data)
        return dish

