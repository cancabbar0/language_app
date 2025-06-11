import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from language_app.models import Words, UserWords, QuestionCount
from .forms import LoginForm, RegisterForm, ForgotPasswordForm


def index(request):
    return render(request, "accounts/index.html")


def login_view(request):
    if request.method == "POST":
        response_data = {}
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is None:
                response_data["error"] = True
                response_data["result"] = "Email or password is wrong"
            else:
                login(request, user)
                response_data["redirect_url"] = reverse("home")
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("index")


def register_view(request):
    if request.method == "POST":
        response_data = {}
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            try:
                user = User.objects.create(username=username, email=email)
                user.set_password(password)
                user.save()

                # kullanıcıya ait userwords kelimelerini tabloya ekle
                words = Words.objects.all()
                for word in words:
                    userwords = UserWords.objects.create(user_id=user.id, word_id=word.id)
                    userwords.save()

                # kullanıcıya ait question count u tabloya ekle
                question_count = QuestionCount.objects.create(user_id=user.id, ask_count=10)
                question_count.save()

                response_data["error"] = False
                response_data["result"] = "Kullanıcı başarı ile oluşturuldu"
            except Exception as e:
                response_data["error"] = True
                response_data["result"] = str(e)
        else:
            response_data["error"] = True
            response_data["result"] = "form is invalid"

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return render(request, "accounts/register.html")


def forgot_password_view(request):
    if request.method == "POST":
        response_data = {}
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")

            try:
                user = User.objects.get(username=username)
                if user is not None:
                    response_data["error"] = False
                    response_data["result"] = "We sent an email to your email address. Please check your inbox."
                else:
                    response_data["error"] = True
                    response_data["result"] = "username not found"
            except ObjectDoesNotExist:
                response_data["error"] = True
                response_data["result"] = "username not found"
            except Exception as e:
                response_data["error"] = True
                response_data["result"] = str(e)
        else:
            response_data["error"] = True
            response_data["result"] = "form is invalid"

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return render(request, "accounts/forgot_password.html")
