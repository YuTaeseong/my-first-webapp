from django import forms
from .models import Site_Name
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField


class CreateUserForm(UserCreationForm):  # 내장 회원가입 폼을 상속받아서 확장한다.
    email = forms.EmailField(required=True)  # 이메일 필드 추가

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2",)
        field_classes = {'username': UsernameField}

    def save(self, commit=True):  # 저장하는 부분 오버라이딩
        user = super(UserCreationForm, self).save(commit=False)  # 본인의 부모를 호출해서 저장하겠다.

        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user