from django.contrib.auth import login, authenticate, logout
from .models import Brand, Color, Car, Comment
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import CommentForm, RegisterForm, LoginForm


# Create your views here.


def home(request:HttpRequest):
    brands = Brand.objects.all()
    colors = Color.objects.all()
    cars = Car.objects.all()
    context = {
        "brands": brands,
        "colors": colors,
        "cars": cars
    }
    return render(request, 'index.html', context)

# ---------------------------------------CRUD------------------------------------

def car_detail(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    comments = car.comments.all()
    form = CommentForm()
    context = {
        "car": car,
        "comments": comments,
        "form": form
    }
    return render(request, "car_detail.html", context)


def add_comment(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "To add a comment, please register!")
            return redirect("login")

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.car = car
            comment.save()
            messages.success(request, "Comment added successfully! 👌")
            return redirect("car_detail", car_id=car.id)
        else:
            messages.error(request, "Error adding comment 😞")
    else:
        form = CommentForm()

    return render(request, "add_car.html", context={"form": form})


def update_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.user_name != request.user.user_name:
        messages.error(request, "You can only update your own comments!")
        return redirect("car_detail", car_id=comment.car.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Update comment ✏")
            return redirect("car_detail", car_id=comment.car.id)
        else:
            messages.error(request, "Error update 🙃🙃🙃")
    else:
        form = CommentForm(instance=comment)

    return render(request, "update_car.html", context={"form": form, "comment": comment})


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk= comment_id)

    if not request.user.is_authenticated:
        messages.error(request, "To delete comments, please login!")
        return redirect("login")

    if comment.user_name != request.user.user_name:
        messages.error(request, "You can only delete your own comments!")
        return redirect("car_detail", car_id=comment.car.id)

    car_id = comment.car.id
    comment.delete()
    messages.success(request, "Success deleted! 🗑")
    return redirect("car_detail", car_id=car_id)


# ---------------------------------------FILTER------------------------------------

def cars_by_color(request, color_id):
    color = get_object_or_404(Color, pk=color_id)
    cars = Car.objects.filter(color=color)
    context = {
        "color": color,
        "cars": cars
    }
    return render(request, "filter_detail.html", context)


def cars_by_brand(request, brand_id):
    brand = get_object_or_404(Brand, pk=brand_id)
    cars = Car.objects.filter(brand=brand)
    context = {
        "brand": brand,
        "cars": cars
    }
    return render(request, "filter_detail.html", context)


# ---------------------------------------AUTH------------------------------------

def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful! 🥳\n"
                                      "Please enter your username and password to log in!")
            return redirect("login")
        else:
            messages.error(request, "Error during registration! 😞")
    else:
        form = RegisterForm()

    context = {
        "form": form
    }
    return render(request, "auth/register.html", context)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Logged in successfully! {user.username} 😊")
            return redirect("home")
        else:
            messages.error(request, "Invalid login credentials! 😞")
    else:
        form = LoginForm()

    context = {
        "form": form
    }
    return render(request, "auth/login.html", context)


def user_logout(request):
    logout(request)
    messages.warning(request, "You have been logged out of your account! ☹")
    return redirect("login")