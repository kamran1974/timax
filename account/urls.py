from django.urls import path

from account import views

app_name="account"
urlpatterns = [
    path('', views.LoginView.as_view(), name='login_page'),

]