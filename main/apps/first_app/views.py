from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'first_app/index.html')

def process(request):
    if request.method == 'POST':
        errors = User.objects.validator(request.POST)
        # checking if there are any errors
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            # this redirects to the user form so they can reenter the correct information
            return redirect(index)
        #  if there are no errors, we will continue by hashing the password and entering that information into the DB
        else: 
            hash1= bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user = User(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = hash1)
            user.save()
        # information that was posted, we will not put into session
            request.session['id'] = user.id
            request.session['name'] = user.first_name 
            messages.success(request, "Registration was successful")
            return redirect(index)
    

def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validation(request.POST)
        #  checks if there are any errors while trying to login in
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(index)
        email = request.POST['email']
        user = User.objects.get(email = email)
        request.session['id'] = User.objects.get(email = email).id
        request.session['first_name'] = User.objects.get(email = email).first_name
        return redirect('/success')
            
          
def success(request):
    if 'id' in request.session:
        return render(request, 'first_app/result.html')
    else: messages.error(request, 'You are not logged in, please log in')
    return redirect(index)


