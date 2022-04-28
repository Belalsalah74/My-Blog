from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth.models import User
from django import forms

from accounts.models import Profile

class PassChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['oldpassword','password1','password2']
    
    

class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(required=False)
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email']

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'autocomlpete':'off'})
        self.fields['username'].widget.attrs.update({'autocomlpete':'off'})


    

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email']

    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'autocomlpete':'off'})
        self.fields['username'].widget.attrs.update(autocomplete='off')

class ProfileUpdate_CreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['img']
        

# class LoginForm(forms.Form):
#     username = forms.CharField(max_length=255,required=True)
#     password = forms.CharField(max_length=255,required=True,show_hidden_initial=False)



#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs.update({'placeholder':'enter your name bitch'})




# class UserLogin(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username','password']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs.update({'placeholder':'enter your name bitch'})

#         self.fields['item'].widget.attrs.update({'placeholder':'Enter ingredient name'})