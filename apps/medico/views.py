from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Especialidades, DadosMedico, DatasAbertas
from paciente.models import Consulta, Documento
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncDate


def is_medico(request):
    return DadosMedico.objects.filter(user=request.user).exists()


@login_required
def cadastro_medico(request):

    if is_medico(request):
        messages.add_message(request, constants.WARNING, 'Você já é um médico cadastrado.')
        return redirect('/medicos/abrir_horario')

    if request.method == "GET":
        especialidades = Especialidades.objects.all()
        return render(request, 'medicos/cadastro_medico.html', locals())

    elif request.method == "POST":
        crm = request.POST.get('crm')
        nome = request.POST.get('nome')
        sexo = request.POST.get('sexo')
        cep = request.POST.get('cep')
        rua = request.POST.get('rua')
        bairro = request.POST.get('bairro')
        numero = request.POST.get('numero')
        cim = request.FILES.get('cim')
        rg = request.FILES.get('rg')
        foto = request.FILES.get('foto')
        especialidade = request.POST.get('especialidade')
        descricao = request.POST.get('descricao')
        valor_consulta = request.POST.get('valor_consulta')

        # TODO: Validar todos os campos
        dados_medico = DadosMedico(
            crm=crm,
            nome=nome,
            sexo=sexo,
            cep=cep,
            rua=rua,
            bairro=bairro,
            numero=numero,
            rg=rg,
            cedula_identidade_medica=cim,
            foto=foto,
            user=request.user,
            descricao=descricao,
            especialidade_id=especialidade,
            valor_consulta=valor_consulta
        )

        dados_medico.save()
        messages.add_message(request, constants.SUCCESS, 'Cadastro médico realizado com sucesso.')
        return redirect('/medicos/abrir_horario')


@login_required
def abrir_horario(request):
    eh_medico = is_medico(request)

    if not is_medico(request):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
        return redirect('/usuarios/logout')

    if request.method == "GET":
        dados_medicos = DadosMedico.objects.get(user=request.user)
        datas_abertas = DatasAbertas.objects.filter(user=request.user).order_by('data')
        return render(request, 'medicos/abrir_horario.html', locals())

    elif request.method == "POST":
        data = request.POST.get('data')

        data_formatada = datetime.strptime(data, "%Y-%m-%dT%H:%M")

        if data_formatada <= datetime.now():
            messages.add_message(request, constants.WARNING, 'A data deve ser maior ou igual a data atual.')
            return redirect('/medicos/abrir_horario')

        horario_abrir = DatasAbertas(
            data=data,
            user=request.user
        )

        horario_abrir.save()

        messages.add_message(request, constants.SUCCESS, 'Horário cadastrado com sucesso.')
        return redirect('/medicos/abrir_horario')


@login_required
def consultas_medico(request):
    if not is_medico(request):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
        return redirect('/usuarios/logout')

    hoje = datetime.now().date()

    consultas_hoje = Consulta.objects.filter(data_aberta__user=request.user).filter(data_aberta__data__gte=hoje).filter(
        data_aberta__data__lt=hoje + timedelta(days=1))
    consultas_restantes = Consulta.objects.exclude(id__in=consultas_hoje.values('id'))

    return render(request, 'medicos/consultas_medico.html',{'consultas_hoje': consultas_hoje,
                                                    'consultas_restantes': consultas_restantes,
                                                    'eh_medico': is_medico(request)})


@login_required
def consulta_area_medico(request, id_consulta):
    if not is_medico(request):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
        return redirect('/usuarios/logout')

    if request.method == "GET":
        eh_medico = is_medico(request)
        consulta = Consulta.objects.get(id=id_consulta)
        documentos = Documento.objects.filter(consulta=consulta)
        return render(request, 'medicos/consulta_area_medico.html', locals())

    elif request.method == "POST":
        # Inicializa a consulta + link da chamada
        consulta = Consulta.objects.get(id=id_consulta)
        link = request.POST.get('link')

        if consulta.status == 'C':
            messages.add_message(request, constants.WARNING, 'Essa consulta já foi cancelada, você não pode inicia-la')
            return redirect(f'/medicos/consulta_area_medico/{id_consulta}')
        elif consulta.status == "F":
            messages.add_message(request, constants.WARNING, 'Essa consulta já foi finalizada, você não pode inicia-la')
            return redirect(f'/medicos/consulta_area_medico/{id_consulta}')

        consulta.link = link
        consulta.status = 'I'
        consulta.save()

        messages.add_message(request, constants.SUCCESS, 'Consulta inicializada com sucesso.')
        return redirect(f'/medicos/consulta_area_medico/{id_consulta}')


@login_required
def finalizar_consulta(request, id_consulta):
    if not is_medico(request):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
        return redirect('/usuarios/logout')

    consulta = Consulta.objects.get(id=id_consulta)
    if request.user != consulta.data_aberta.user:
        messages.add_message(request, constants.WARNING, 'Você não pode finalizar uma consulta que não é sua')
        return redirect(f'/medicos/consulta_area_medico/{id_consulta}')
    consulta.status = 'F'
    consulta.save()
    return redirect(f'/medicos/consulta_area_medico/{id_consulta}')

@login_required
def add_documento(request, id_consulta):
    if not is_medico(request):
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
        return redirect('/usuarios/logout')

    consulta = Consulta.objects.get(id=id_consulta)

    if consulta.data_aberta.user != request.user:
        messages.add_message(request, constants.ERROR, 'Essa consulta não é sua!')
        return redirect(f'/medicos/consulta_area_medico/{id_consulta}')

    titulo = request.POST.get('titulo')
    documento = request.FILES.get('documento')

    if not documento:
        messages.add_message(request, constants.WARNING, 'Adicione o documento.')
        return redirect(f'/medicos/consulta_area_medico/{id_consulta}')

    documento = Documento(
        consulta=consulta,
        titulo=titulo,
        documento=documento

    )

    documento.save()

    messages.add_message(request, constants.SUCCESS, 'Documento enviado com sucesso!')
    return redirect(f'/medicos/consulta_area_medico/{id_consulta}')


@login_required
def dashboard(request):
    eh_medico = is_medico(request)
    if not eh_medico:
        messages.add_message(request, constants.WARNING, 'Somente médicos podem acessar essa página.')
        return redirect('/usuarios/logout')

    # Verificar se o usuário forneceu um período personalizado
    dias = request.GET.get('dias', None)
    data_inicio = timezone.now() - timedelta(days=7)
    data_fim = timezone.now()

    if dias:
        if dias == '30':
            data_inicio = timezone.now() - timedelta(days=30)
            data_fim = timezone.now()
        elif dias == '15':
            data_inicio = timezone.now() - timedelta(days=15)
            data_fim = timezone.now()

    consultas = Consulta.objects.filter(
        medico__user=request.user,
        data_aberta__data__range=[data_inicio, data_fim],
        status='F'
    ).annotate(data_somente=TruncDate('data_aberta__data')).values('data_somente').annotate(quantidade=Count('id')).order_by('data_somente')

    datas = [consulta['data_somente'].strftime('%d/%m') for consulta in consultas]
    quantidade = [consulta['quantidade'] for consulta in consultas]

    return render(request, 'medicos/dashboard.html', {
        'datas': datas,
        'quantidade': quantidade,
        'eh_medico': eh_medico,
    })