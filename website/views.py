from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record
# Create your views here.


def home(request):
    records = Record.objects.all()

    # check to see if logging in
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # authnticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "you have been loged in")
            return redirect('home')
        else:
            messages.success(request, "there was an error")
            return redirect('home')

    return render(request, 'home.html', {'records': records})


def logout_user(request):
    logout(request)
    messages.success(request, "you have been logged out")
    return redirect("home")


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
        # authenticate and login

        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']

        user = authenticate(request, username=username, password=password)
        login(request, user)
        messages.success(request, "you have successfully registerd")
        return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        # lookup record
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.success(request, 'you have to login to view the records')
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        # deleting record
        delete_record = Record.objects.get(id=pk)
        delete_record.delete()
        messages.success(request, "You have succesfully delete the record")
        return redirect('home')
    else:
        messages.success(request, "You have to Login to delete the users")
        return redirect('home')


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        # add the record
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(
                    request, "you have successfully added the record")
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})

    else:
        messages.success(request, "you have to login to add new record")
        return redirect("home")


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "you have successfully updated")
                return redirect('home')
        return render(request, 'updated_record.html', {'form': form})
    else:
        messages.success(request, "you have to login to update the record")
        return redirect('home')
