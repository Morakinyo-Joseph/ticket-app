from django.shortcuts import render, redirect
from .models import Game, History
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import GameCreateForm
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from .models import User
import re

# Create your views here.


@login_required
def home(request):
    slip = ""
    if request.method == "POST":
        code = request.POST["code"]

        if Game.objects.filter(ticket_ID=code).exists():
            slip = Game.objects.get(ticket_ID=code)
            print(slip)
        elif code == "":
            messages.info(request, "input cannot be empty")
            return redirect("core:home")
        else:
            messages.info(request, "invalid code")
            return redirect("core:home")

    return render(request, "core/home.html", {"slip": slip})


def signin(request):
    if request.user.is_authenticated:
        return redirect("core:home")

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        the_user = authenticate(username=username, password=password)

        if the_user != None:
            login(request, the_user)
            messages.success(request, "log in successful")
            return redirect('core:home')
        else:
            messages.info(request, "Email/Password doesn't exists")

    return render(request, "core/login.html")


def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        ig_handle = request.POST['instagram_handle']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if first_name == "":
            messages.info(request, 'Name cannot be null')
            return redirect("core:signup")

        elif last_name == "":
            messages.info(request, 'Name cannot be null')
            return redirect("core:signup")

        elif pass1 == pass2:
            username = first_name + "." + last_name

            if User.objects.filter(email=email).exists(): 
                messages.info(request, "Email address already exists!")
                return redirect('core:signup')
            else:
                the_user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, ig_handle=ig_handle, email=email, password=pass1)
                the_user.save()

                logged_user = authenticate(username=username, password=pass1)

                if logged_user != None:
                    login(request, logged_user)
                    messages.success(request, "Account Creation successful")
                    return redirect('core:home')
                else:
                    messages.error(request, "Couldn't log you in, kindly contact customer care")
                    return redirect("core:login")

        
        else:
            messages.info(request, 'Passwords do not match!')
            return redirect('core:signup')

    return render(request, 'core/signup.html')


def log_out(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("core:home")


@login_required
def posting(request):
    form = GameCreateForm()
    if request.method == "POST":
        form = GameCreateForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['ticket_ID']
            code = form.cleaned_data['booking_code']
            odds = form.cleaned_data['odds']
            remark = form.cleaned_data['remarks']

            new_game = Game.objects.create(ticket_ID=id, booking_code=code, odds=odds, remarks=remark)
            new_game.save()

            history = History.objects.create(ticket_ID=id, booking_code=code, odds=odds, remarks=remark)
            history.save()

            messages.info(request, "Game posted successfully")
            return redirect('core:post')
        else:
            messages.info(request, "Error in form inputation")
            return redirect("core:post")
            
    return render(request, "core/posting.html", {"form": form})


@login_required
def deletion(request, pk):
    game = Game.objects.get(id=pk)
    game.delete()
    
    return redirect("core:list")


@login_required
def list(request):
    void = True
    game = Game.objects.all()
    current_date = datetime.now()
    for g in game:
        if g:
            void = False

    print(void)

    return render(request, "core/list.html", {"game": game, "current_date": current_date, "void": void})    



def error_404(request, exception):
    return render(request, "core/404.html")


def error_500(request):
    return render(request, "core/500.html")