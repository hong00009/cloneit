from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if  form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movies:index')
    else:
        form = CustomUserCreationForm()

    context = {
        'form' : form
    }

    return render(request, 'accounts/form.html', context)


def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('movies:index')
        
    else:
        form = CustomAuthenticationForm()

    context = {
        'form' : form,
    }

    return render(request, 'accounts/form.html', context)

def logout(request):
    auth_logout(request)
    return redirect('accounts:login')


@login_required
def comment_list(request):
    comments = request.user.like_set.all().order_by('-created_at')

    context = {
        'comments': comments,
    }

    return render(request, 'accounts/comment_list.html', context)


def profile(request, username):
    User = get_user_model()
    user_info = get_object_or_404(User, username=username)

    comments = user_info.comments.all().order_by('-created_at')

    context = {
        'user_info': user_info,
        'comments': comments,
    }

    return render(request, 'accounts/profile.html', context)