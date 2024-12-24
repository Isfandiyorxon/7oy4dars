
from .views import home,dish_detaling,dish_to_category,add_dish,update_dish,delate_dish
from django.urls import path

urlpatterns=[
path('',home,name='home'),
path('dish_to_category/<int:pk>/',dish_to_category,name='dish_to_category'),
path('dish_detaling/<int:pk>/',dish_detaling,name='dish_detaling'),
path('dish_add/',add_dish,name='add_dish'),
path('dish_update/<int:pk>/',update_dish,name='dish_update'),
path('dish_delete/<int:pk>/',delate_dish,name='delate_dish')
]