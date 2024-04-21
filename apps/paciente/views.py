from django.shortcuts import render
from medico.models import DadosMedico, DatasAbertas, Especialidades
from datetime import datetime

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