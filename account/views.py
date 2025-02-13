from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def register_view(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return redirect('login')
        else:
            return render(request, 'register.html',{'user_form':user_form})
    user_form = UserCreationForm()
    return render(request, 'register.html',{'user_form':user_form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('cars_home')  # Redireciona para a página principal (ou qualquer outra)

        # Se a autenticação falhar, o formulário é retornado com uma mensagem de erro
        login_form = AuthenticationForm()
        return render(request, 'login.html', {'login_form': login_form, 'error': 'Credenciais inválidas'})

    # Se o método for GET, renderiza o formulário de login
    login_form = AuthenticationForm()
    return render(request, 'login.html', {'login_form': login_form})


def logout_view(request):
    logout(request)
    return redirect('cars_home')

