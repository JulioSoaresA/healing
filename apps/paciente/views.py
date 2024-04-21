from django.shortcuts import render
from .models import Consulta
from medico.models import DadosMedico, DatasAbertas, Especialidades
from datetime import datetime
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.messages import constants

def home(request):
    if request.method == "GET":
        medicos = DadosMedico.objects.all()
        especialidades = Especialidades.objects.all()

        medico_filtrar = request.GET.get('medico')
        especialidades_filtrar = request.GET.getlist('especialidades')

        if medico_filtrar:
            medicos = medicos.filter(nome__icontains=medico_filtrar)

        if especialidades_filtrar:
            medicos = medicos.filter(especialidade_id__in=especialidades_filtrar)

        return render(request, 'pacientes/home.html', locals())


def escolher_horario(request, id_dados_medicos):
    if request.method == "GET":
        medico = DadosMedico.objects.get(id=id_dados_medicos)
        datas_abertas = DatasAbertas.objects.filter(user=medico.user, data__gte=datetime.now(), agendado=False)
        return render(request, 'pacientes/escolher_horario.html', locals())


def agendar_horario(request, id_data_aberta):
    if request.method == "GET":
        data_aberta = DatasAbertas.objects.get(id=id_data_aberta)

        horario_agendado = Consulta(
            paciente=request.user,
            data_aberta=data_aberta
        )

        horario_agendado.save()

        data_aberta.agendado = True
        data_aberta.save()

        messages.add_message(request, constants.SUCCESS, 'Horário agendado com sucesso.')

        return redirect('/pacientes/minhas_consultas/')


def minhas_consultas(request):
    if request.method == "GET":
        especialidades = Especialidades.objects.all()
        medicos = DadosMedico.objects.all()
        minhas_consultas = Consulta.objects.filter(paciente=request.user, data_aberta__data__gte=datetime.now())

        especialidades_filtrar = request.GET.get('especialidades')
        data_filtrar = request.GET.get('data')

        if data_filtrar:
            minhas_consultas = minhas_consultas.filter(data_aberta__data__date=data_filtrar)

        if especialidades_filtrar:
            especialidades = Especialidades.objects.filter(especialidade__icontains=especialidades_filtrar)
            medicos = medicos.filter(especialidade__especialidade__icontains=especialidades.values_list('especialidade', flat=True))
            minhas_consultas = minhas_consultas.filter(data_aberta__user__in=medicos.values_list('user', flat=True))


        return render(request, 'pacientes/consultas_medico.html', locals())