from django.contrib.messages import add_message,SUCCESS
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from .forms import ProfileUpdate_CreateForm,UserUpdateForm,UserSignUpForm,PassChangeForm

def profile_view(request,id):
    user = get_object_or_404(User,id=id)
    context = {'profile':user.profile}
    return render(request,'accounts/profile.html',context)



def udpate_profile(request,id):
    user = get_object_or_404(User,id=id)
    profile = user.profile
    user_form = UserUpdateForm(request.POST or None, instance=user)
    profile_form = ProfileUpdate_CreateForm(request.POST or None,request.FILES or None, instance=profile)
    context = {'user_form':user_form,'profile_form':profile_form,'profile':user.profile,'user':user}
    if profile_form.is_valid():
        # print(request.FILES)
        profile_form.save()
        user_form.save()
        add_message(request,SUCCESS,'Profile updated successfully')
        return(redirect(reverse('accounts:profile',args=(id,))))
    return render(request,'accounts/profile_update.html',context)

def PassChange(request,id):
    user = get_object_or_404(User,id=id)
    form = PassChangeForm(user,data=request.POST)
    context = {'user':user,'form':form}
   
    if form.is_valid():
        form.save()
        add_message(request,SUCCESS,'Password updated succesfully')
        login(request,user)
        return redirect('home')
    return render(request,'accounts/password_change.html',context)

def login_try(request):
    
    form = AuthenticationForm(data=request.POST)
    context = {'form':form}
    print(request.GET)
    if form.is_valid():
        user = form.get_user()
        login(request,user)
        if 'next' in request.GET :
            return redirect(request.GET['next'])
        return redirect('home')
    return render(request,'accounts/login.html',context)




def login_try_old(request):
    context = {'title':'login'}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,
        username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            context = {'title':'login','message':'invalid username or password'}
            return render(request,
            'accounts/login.html',context)

    return render(request,'accounts/login.html',context)
    

def logout_try(request):

    if request.POST:
       logout(request)
       return redirect('accounts:login')
    
    return render(request,'accounts/logout.html')   

def register_try(request):
    form = UserSignUpForm(request.POST or None)
    profile_form = ProfileUpdate_CreateForm(request.POST or None,request.FILES or None)
    context = {'form':form,'profile_form':profile_form}
    print(request.GET)
    if form.is_valid() and profile_form.is_valid():
        user = form.save()
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()
        login(request,user)
        if 'next' in request.POST:
            return redirect(request.POST['next'])
        return redirect('home')
    return render(request,'accounts/register.html',context)


# def login_view(request):
    
#     form = UserLogin()
#     c = {'form':form}
#     if request.POST:
#         form = UserLogin(request.POST)
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request,username=username,password=password)
#         login(request,user)
#         return redirect('home')
    
    
    
#     return render(request,'accounts/login.html')



# def logout_view(request):
#     logout(request)
#     return redirect(reverse('home'))

# def register_view(request):
#     form = UserCreationForm()
#     context = {'form':form}
#     if request.POST:
#         form = UserCreationForm(request.POST)
#         form.save()
#         return redirect(reverse('accounts:login'))

#     return render(request,'accounts/register.html',context)
