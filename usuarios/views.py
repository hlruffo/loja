from django.contrib import auth, messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from rolepermissions.decorators import has_permission_decorator

from .models import Users


# Create your views here.
@has_permission_decorator('cadastrar_vendedor')
def cadastrar_vendedor(request):
    if request.method == "GET":
        vendedores = Users.objects.filter(cargo='V')
        return render(request, 'cadastrar_vendedor.html', {'vendedores': vendedores})

    if request.method == "POST":
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = Users.objects.filter(email=email)
        if user.exists():
            # TODO : utilizar message do Django
            return HttpResponse('Email já existe')
        else:
            user = Users.objects.create_user(
                first_name=nome,
                last_name=sobrenome,
                username=email,
                email=email,
                password=senha,
                cargo='V'
            )
        # TODO:redirecionar com uma msg
        return HttpResponse("Conta criada")


def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect(reverse('plataforma.html'))
        return render(request, 'login.html')
    elif request.method == 'POST':
        login = request.POST.get('email')
        senha = request.POST.get('senha')

        user = auth.authenticate(username=login, password=senha)

        if not user:
            # TODO: REDIRECIONAR COM MSG DE ERRO
            return HttpResponse('Usuario inválido')
        auth.login(request, user)
        return HttpResponse('Usuario Logado com successo')


def logout(request):
    request.session.flush()
    return redirect(reverse('login'))


@has_permission_decorator('cadastrar_vendedor')
def excluir_usuario(request, id):
    vendedor = get_object_or_404(Users, id=id)
    vendedor.delete()
    messages.add_message(request, messages.SUCCESS,
                         'Vendedor excluído com successo')
    return redirect(reverse('cadastrar_vendedor'))
