from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET

from .forms import RegistrationForms, LoginForm, EditForm
from .models import User

class UserRegister(View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        request.title = "Ro'yxatdan o'tish"


    def get(self, request):
        form = RegistrationForms()
        request.title = "Ro'yxatdan o'tish"

        return render(request, 'user/registration.html', {
            'form': form
        })

    def post(self, request):
        form = RegistrationForms(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            del data['confirm']
            user = User(**data)
            user.set_password(data['password'])
            user.save()
            messages.success(request, "Siz muvaffaqiyatli ro'yxatdan o'tdingiz.")
            return redirect('name:index')

        return render(request, 'user/registration.html', {
            'form': form
        })

def user_login(request):
    request.title = "Tizimga kirish"

    form = LoginForm()
    if request.POST:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, "Hush kelibsiz!!! {}".format(user.first_name))
                return redirect('name:index')

            form.add_error('password', 'Username va/yoki parol hato ')

    return render(request, 'user/login.html', {
        'form': form
    })

@login_required
def user_logout(request):
    logout(request)
    return redirect('name:index')


@require_GET
@login_required
def user_info(request):
    request.title = "O'zgartirish"
    return render(request, 'user/edit.html', {
        'form': EditForm(instance=request.user)
    })

@require_POST
@login_required
def user_info_post(request):
    form = EditForm(data=request.POST, instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, "Muvaffaqiyatli o'zgartirildi")
        return redirect('name:index')

    return render(request, 'user/edit.html', {
        "form": form}
)