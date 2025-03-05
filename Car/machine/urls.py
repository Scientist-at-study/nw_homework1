from django.urls import path
from .views import (CarListView, CommentCreateView, update_comment, DeleteCommentView,
                    CarsByColor, CarsByBrand, CarDetailView, user_register,
                    user_login, user_logout, SendEmailView)

urlpatterns = [
    path('', CarListView.as_view(), name="home"),
    path('car/<int:car_id>', CarDetailView.as_view(), name="car_detail"),
    path('car/<int:car_id>/comment/add/', CommentCreateView.as_view(), name="add_comment"),
    path("comment/<int:comment_id>/update/", update_comment, name="update_comment"),
    path("comment/<int:comment_id>/delete/", DeleteCommentView.as_view(), name="delete_comment"),
    path('cars/color/<int:color_id>', CarsByColor.as_view(), name="cars_by_color"),
    path('cars/brand/<int:brand_id>', CarsByBrand.as_view(), name="cars_by_brand"),
    path('register/', user_register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    path('send-message/', SendEmailView.as_view(), name='send_message_to_email'),

]
