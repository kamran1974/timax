from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        label='نام کاربری',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کاربری'}),
    )
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'کلمه عبور'}),
    )
