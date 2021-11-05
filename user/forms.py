from django import forms
# from pyfull.validators import PhoneValidator
from django.core.validators import MinLengthValidator   # Validatsiya holatini tekshiramiz
from django.contrib.auth.validators import UnicodeUsernameValidator     # Foydalanuvchini ismini tkshiardi
from django.core.exceptions import ValidationError


from .models import User


class RegistrationForms(forms.Form):
    username = forms.CharField(max_length=20, required=True,
                               validators=[UnicodeUsernameValidator()])
    phone = forms.CharField(max_length=14, required=True)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput, required=True,
                               validators=[MinLengthValidator(6)])
    confirm = forms.CharField(max_length=50, widget=forms.PasswordInput, required=True,
                              validators=[MinLengthValidator(6)])

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Ushbu nom ro'yxatdan o'tgan")
        return self.cleaned_data['username']

    def clean_phone(self):
        phone =self.cleaned_data['phone']
        if User.objects.filter(phone=phone).exists():
            raise ValidationError("Ushbu raqam ro'yxatdan o'tgan")
        return self.cleaned_data['phone']

    def clean_confirm(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm']:
            raise ValidationError("Parollar bir xil emas")
        return self.cleaned_data['confirm']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)


class EditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'phone', 'last_name', 'email']