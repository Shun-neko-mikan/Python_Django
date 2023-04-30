from django import forms
from django.contrib.auth.models import User
from .models import Account , DLurls

class AccountForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label = "パスワード")

    class Meta:
        model = User
        fields = ("username", "email", "password")

        labels = {"username": "ユーザー名", "email": "メールアドレス"}
    
class AddAccountForm(forms.ModelForm):
    class Meta():
        model = Account
        fields = ("last_name", "first_name", "account_image")

        labels = {"last_name": "姓", "first_name": "名", "account_image": "アカウント画像"}

class DLForm(forms.ModelForm):
    class Meta():
        model = DLurls
        fields = ("website",)
        labels = {"website": "URL"}