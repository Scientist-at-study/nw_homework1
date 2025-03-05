import time

from django.contrib.auth import login, authenticate, logout
from django.http import HttpRequest, HttpResponse
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


from .models import Brand, Color, Car, Comment
from .forms import CommentForm, RegisterForm, LoginForm, SendEmail


# Create your views here.


class CarListView(ListView):
    model = Car
    # template_name = "index.html"
    context_object_name = "cars"
    extra_context = {
        "title": "Asosiy sahifa"
    }

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data()
    #     context["my_brands"] = Brand.objects.all()
    #     return context

# def home(request:HttpRequest):
#     # brands = Brand.objects.all()
#     # colors = Color.objects.all()
#     cars = Car.objects.all()
#     context = {
#         # "brands": brands,
#         # "colors": colors,
#         "cars": cars
#     }
#     return render(request, 'index.html', context)

# ---------------------------------------CRUD------------------------------------


class CarDetailView(DetailView):
    model = Car
    context_object_name = "car"
    pk_url_kwarg = "car_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = Comment.objects.all()
        # context["comments"] = Comment.objects.filter(car=self.object)
        # context["form"] = CommentForm()
        return context


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


class CommentCreateView(CreateView):
    model = Comment
    fields = ['comment']
    template_name = "add_comment.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.car = Car.objects.get(id=self.kwargs['car_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('car_detail', kwargs={'car_id': self.object.car.id})





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

    return render(request, "add_comment.html", context={"form": form})


def update_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.username != request.user.username:
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

    return render(request, "update_comment.html", context={"form": form, "comment": comment})


class DeleteCommentView(DeleteView):
    model = Comment
    pk_url_kwarg = "comment_id"
    # template_name = "confirm_delete.html"
    context_object_name = "car"
    success_url = reverse_lazy('home')



def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if not request.user.is_authenticated:
        messages.error(request, "To delete comments, please login!")
        return redirect("login")

    if comment.username != request.user.username:
        messages.error(request, "You can only delete your own comments!")
        return redirect("car_detail", car_id=comment.car.id)

    car_id = comment.car.id
    comment.delete()
    messages.success(request, "Success deleted! 🗑")
    return redirect("car_detail", car_id=car_id)


# ---------------------------------------FILTER------------------------------------

class CarsByColor(CarListView):
    def get_queryset(self):
        return Car.objects.filter(color_id=self.kwargs.get("color_id"))


def cars_by_color(request, color_id):
    color = get_object_or_404(Color, pk=color_id)
    cars = Car.objects.filter(color=color)
    context = {
        "color": color,
        "cars": cars
    }
    return render(request, "filter_detail.html", context)


class CarsByBrand(CarListView):
    def get_queryset(self):
        return Car.objects.filter(brand_id=self.kwargs.get("brand_id"))


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


# ----------------------------------------SEND EMAIL--------------------------------------

class SendEmailView(View):
    def post(self, request):
        form = SendEmail(data=request.POST)
        if form.is_valid():
            subject = form.cleaned_data.get("subject")
            message = form.cleaned_data.get("message")
            for user in User.objects.all():
                mail = send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email]
                )
                time.sleep(0.5)
                print(mail, "----------------------------")
        messages.success(request, "Sending news!!!")
        return redirect("home")

    def get(self, request):
        form = SendEmail()
        context = {
            "form": form
        }
        return render(request, "send_mail.html", context)


# def send_message_to_email(request):
#     if request.method == 'POST':
#         form = SendEmail(data=request.POST)
#         if form.is_valid():
#             subject = form.cleaned_data.get("subject")
#             message = form.cleaned_data.get("message")
#             for user in User.objects.all():
#                 mail = send_mail(
#                     subject=subject,
#                     message=message,
#                     from_email=settings.EMAIL_HOST_USER,
#                     recipient_list=[user.email]
#                 )
#                 time.sleep(0.5)
#                 print(mail, "----------------------------")
#         messages.success(request, "Sending news!!!")
#         return redirect("home")
#     else:
#         form = SendEmail()
#     context = {
#         "form": form
#     }
#     return render(request, "send_mail.html", context)