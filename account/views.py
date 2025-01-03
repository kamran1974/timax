from django.contrib.auth.decorators import login_required


from django.contrib.auth import authenticate, login ,logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest
from django.views import View
from .forms import LoginForm

class LoginView(View):  # login view
    def get(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('inout:worklog_report'))

        login_form = LoginForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'account/login.html', context=context)

    def post(self, request: HttpRequest):
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is None:
                login_form.add_error('username', 'نام کاربری یا کلمه عبور اشتباه است.')
            elif not user.is_active:
                login_form.add_error('username', 'حساب کاربری شما فعال نیست.')
            else:
                login(request, user)
                return redirect(reverse('inout:worklog_report'))
        context = {
            'login_form': login_form
        }
        return render(request, 'account/login.html', context=context)




class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('account:login_page'))


