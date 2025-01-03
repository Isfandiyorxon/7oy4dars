
from .views import (home,dish_detaling,dish_to_category,add_dish,update_dish,delate_dish,register,login_view,logout_view,
                    comment_save,delete_comment,send_message_email)
from django.urls import path

urlpatterns=[
path('',home,name='home'),
path('dish_to_category/<int:pk>/',dish_to_category,name='dish_to_category'),
path('dish_detaling/<int:pk>/',dish_detaling,name='dish_detaling'),

path('dish_add/',add_dish,name='add_dish'),
path('dish_update/<int:pk>/',update_dish,name='dish_update'),
path('dish_delete/<int:pk>/',delate_dish,name='delate_dish'),

path('register/', register, name='register'),
path('login/', login_view, name='login'),
path('logout/', logout_view, name='logout'),

path('dish_add_commnet/<dish_id>/',comment_save,name='comment_save'),
path('dish_delete_commnet/<dish_id>/<int:post_id>',delete_comment,name='delete_comment'),
path('send/email/',send_message_email)


]


