from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

from accounts.models import Profile


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-3 form-control-lg', 'placeholder': 'Username'})

        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3 form-control-lg', 'placeholder': 'Enter password'})

        for field in self.fields:
            self.fields[field].label = ''
            self.fields[field].help_text = ''


class UserSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'class': 'form-control mb-3 form-control-lg', 'placeholder':  self.fields[field].label})
            self.fields[field].label = ''
            self.fields[field].help_text = ''


class PassChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['oldpassword', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'class': 'form-control mb-3 form-control-lg', 'placeholder':self.fields[field].label})
            self.fields[field].label = ''
            self.fields[field].help_text = ''




class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'class': 'form-control mb-3 form-control-lg', 'placeholder':  self.fields[field].label})
            self.fields[field].label = ''
            self.fields[field].help_text = ''



class ProfileUpdate_CreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','img']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['img'].widget.attrs.update(
            {'class': 'form-control mb-3 form-control-lg','placeholder':'choose profile pic'})
        self.fields['bio'].widget.attrs.update(
            {'class': 'form-control mb-3 form-control-lg','placeholder':'Bio..'})
        self.fields['img'].label = ''
        self.fields['bio'].label = ''


