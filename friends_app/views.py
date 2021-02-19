from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import UserManager, User

def home_reroute(request):
    return redirect('/main')

def login(request):
    return render(request, "main.html")

def register(request):
    if request.method=='POST':
        errors=User.objects.validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/main')

        user_pw=request.POST['pw']
        hash_pw=bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
        print(hash_pw)
        new_user = User.objects.create(first_name=request.POST['f_n'], last_name=request.POST['l_n'], email=request.POST['email'], password=hash_pw, birthday=request.POST['bh'])
        print(new_user)
        request.session['user_id']=new_user.id
        request.session['user_name']=f"{new_user.first_name} {new_user.last_name}"
        return redirect('/friends')
    return redirect('/main')

def log_in(request):
    if request.method=='POST':
        logged_user=User.objects.filter(email=request.POST['email'])
        if logged_user:
            logged_user=logged_user[0]
            if bcrypt.checkpw(request.POST['pw'].encode(), logged_user.password.encode()):
                request.session['user_id']=logged_user.id
                request.session['user_name']=f"{logged_user.first_name} {logged_user.last_name}"
                return redirect('/friends')
            else:
                messages.error(request, "Password was incorrect.")
        else:
            messages.error(request, "Email was not found.")
    return redirect('/main')

def  sucess(request):
    if 'user_id' not in request.session:
        return redirect('/main')
    return render(request, "friends.html")

def logout(request):
    request.session.clear()
    return redirect('/main')

def friends(request):
    context = {
        'all_users':User.objects.all()
    }
    return render(request, 'friends.html', context)

def add(request):
    return redirect('/friends')

def profile(request, user_id):
    context = {
        'user': User.objects.get(id=user_id)
    }
    return render(request, 'profile.html', context)

