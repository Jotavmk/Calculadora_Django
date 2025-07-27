from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Usuario
from django.contrib.auth.decorators import login_required
from .models import Operacao

# View de registro

def register_view(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('password')
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado.')
            return redirect('register')
        user = Usuario.objects.create_user(email=email, nome=nome, senha=senha)
        login(request, user)
        return redirect('calculator')
    return render(request, 'calc/register.html')

# View de login

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('password')
        user = authenticate(request, email=email, password=senha)
        if user is not None:
            login(request, user)
            return redirect('calculator')
        else:
            messages.error(request, 'Email ou senha inválidos.')
            return redirect('login')
    return render(request, 'calc/login.html')

# View de logout

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def calculator(request):
    if request.method == 'POST':
        number1 = request.POST.get('number1', '')
        number2 = request.POST.get('number2', '')
        operation = request.POST.get('operation', '')
        if not (number1 and operation):
            return redirect('calculator')
        try:
            n1 = float(number1)
            n2 = float(number2) if number2 else None
        except ValueError:
            return redirect('calculator')
        if operation == '+':
            result = n1 + n2
            parametros = f"{number1}+{number2}"
        elif operation == '-':
            result = n1 - n2
            parametros = f"{number1}-{number2}"
        elif operation == '*':
            result = n1 * n2
            parametros = f"{number1}*{number2}"
        elif operation == '/':
            result = n1 / n2 if n2 != 0 else 'Erro'
            parametros = f"{number1}/{number2}"
        elif operation == '%':
            # Se só n1, retorna n1/100. Se n2, retorna n1 * n2 / 100 (regra de porcentagem)
            if number2:
                result = n1 * (n2 / 100)
                parametros = f"{number1}%{number2}"
            else:
                result = n1 / 100
                parametros = f"{number1}%"
        else:
            result = 'Erro'
            parametros = f"{number1}{operation}{number2}"
        if result != 'Erro':
            Operacao.objects.create(
                usuario=request.user,
                parametros=parametros,
                resultado=str(result)
            )
        return redirect('calculator')
    historico = Operacao.objects.filter(usuario=request.user).order_by('-dt_inclusao')[:10]
    return render(request, 'calc/calculator.html', {'historico': historico})
