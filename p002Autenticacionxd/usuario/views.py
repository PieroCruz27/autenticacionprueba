from django.shortcuts import render
from .form import LoginForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.contrib import messages


from .form import UserRegistrationForm, UserEditForm, LoginForm, ProfileEditForm
from .models import Profile

# Create your views here.


# Vista para manejar el login
def user_login(request):
    if request.method == 'POST':  # Corrección: Debe ser 'request.method' y no 'request'
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    
                    return HttpResponse('Usuario autenticado')
                else:
                    return HttpResponse('Usuario inactivo')
            else:  # Corrección de indentación y sintaxis
                return HttpResponse('Usuario no encontrado')

    else:  # Corrección: faltaba ':'
        form = LoginForm()  # Instanciamos el formulario
    return render(request, 'account/login.html', {'form': form})  # Corrección de indentación



@login_required
def dashboard(request):
   return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user}) #username servira para poner el nomnre del user creado
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form':user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Perfil actualizado', 'succesful')
        else:
            messages.error(request, 'Error al actualizar el perfil')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html',{
        'user_form':user_form,
        'profile_form':profile_form
    })