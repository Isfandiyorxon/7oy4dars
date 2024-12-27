from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=150,unique=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = 'Kategoriyalar'
class Dish (models.Model):
    name=models.CharField(max_length=200,verbose_name='ovqat nomi')
    category=models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name='ovqat turi')
    about=models.TextField(null=True,blank=True , verbose_name='ovqat haqida')
    photo=models.ImageField(upload_to='media/photos/')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ovqat'
        verbose_name_plural = 'Ovqatlar'


class Coments(models.Model):
    text=models.CharField(max_length=1000,verbose_name='koment matni')
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    dish=models.ForeignKey(Dish,on_delete=models.SET_NULL,null=True,verbose_name='Ovqat')
    created=models.DateTimeField(auto_now_add=True,verbose_name="qo'shilgan vaqti")
    def __str__(self):
        return f"{self.user.username}:{self.text[:10]}"


    class Meta:
        verbose_name='komentariya'
        verbose_name_plural='komentariyalar'
        ordering = ['-created']

