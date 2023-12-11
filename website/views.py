from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record
from django.core.paginator import Paginator


# Create your views here.
def home(request):
    # check to see if logging in
    if request.method == "POST":
        username: str = request.POST["username"]
        password: str = request.POST["password"]
        # authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in")
            return redirect("home")
        else:
            messages.error(request, "There was an error logging in. Please try again")
            return redirect("home")

    p = Paginator(Record.objects.all(), 2)
    page = request.GET.get("page")
    records_paginated = p.get_page(page)
    return render(
        request,
        "home.html",
        {"records_paginated": records_paginated},
    )


# def login_user(request):
# if request.method == "POST":
#     username: str = request.POST["username"]
#     password: str = request.POST["password"]
#     # authenticate
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         messages.success(request, "You have been logged in")
#         return redirect("home")
#     else:
#         messages.error(request, "There was an error logging in. Please try again")
#         return redirect("home")
# else:
#     return render(request, "home.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect("home")


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered! Welcome!")
            return redirect("home")
        return render(request, "register.html", {"form": form})
    form = SignUpForm()
    return render(request, "register.html", {"form": form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        # Lookup record
        customer_record = Record.objects.get(id=pk)
        return render(request, "record.html", {"customer_record": customer_record})
    messages.success(request, "You must be logged in to view that page")
    return redirect("home")


def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "You have succesfully deleted the record")
        return redirect("home")
    messages.success(request, "You must be logged in to view that page")
    return redirect("home")


def add_record(request):
    form = AddRecordForm(request.POST or None, request.FILES or None)
    if request.user.is_authenticated:
        print(request.method, form.is_valid())
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Record Added...")
                return redirect("home")
        return render(request, "add_record.html", {"form": form})
    messages.success(request, "You Must Be Logged In...")
    return redirect("home")


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(
            request.POST or None, request.FILES or None, instance=current_record
        )
        print(request.method, form.is_valid())
        if form.is_valid():
            form.save()
            messages.success(request, "Record has been Updated")
            return redirect("home")
        return render(request, "update_record.html", {"form": form})
    messages.success(request, "You Must Be Logged In...")
    return redirect("home")
