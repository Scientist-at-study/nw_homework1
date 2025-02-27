from django.urls import path
from .views import (home, add_comment, update_comment, delete_comment,
                    cars_by_color, cars_by_brand, car_detail, user_register,
                    user_login, user_logout)

urlpatterns = [
    path('', home, name="home"),
    path('car/<int:car_id>', car_detail, name="car_detail"),
    path("car/<int:car_id>/comment/add/", add_comment, name="add_comment"),
    path("comment/<int:comment_id>/update/", update_comment, name="update_comment"),
    path("comment/<int:comment_id>/delete/", delete_comment, name="delete_comment"),
    path('cars/color/<int:color_id>', cars_by_color, name="cars_by_color"),
    path('cars/brand/<int:brand_id>', cars_by_brand, name="cars_by_brand"),
    path('register/', user_register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout')

]
