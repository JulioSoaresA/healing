from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'usuarios/cadastro.html')
    elif request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        senha = request.POST['senha']
        confirmar_senha = request.POST['confirmar_senha']

        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As senhas não conferem')
            return redirect('/usuarios/cadastro/')

        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, 'A senha deve possuir pelo menos 6 caracteres')
            return redirect('/usuarios/cadastro/')

        users = User.objects.filter(username=username)

        if users.exists():
            messages.add_message(request, constants.ERROR, 'Usuário já existe')
            return redirect('/usuarios/cadastro/')

        user = User.objects.create_user(username, email, senha)
        
        return HttpResponse('Usuário cadastrado com sucesso!')