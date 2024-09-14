from django.db import models
from medico.models import DatasAbertas
from django.contrib.auth.models import User
from medico.models import DadosMedico
from django.utils import timezone

class Consulta(models.Model):
    status_choices = (
        ('A', 'Agendada'),
        ('F', 'Finalizada'),
        ('C', 'Cancelada'),
        ('I', 'Iniciada')

    )
    paciente = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    medico = models.ForeignKey(DadosMedico, on_delete=models.DO_NOTHING)
    data_aberta = models.ForeignKey(DatasAbertas, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=1, choices=status_choices, default='A')
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.paciente.username
    
    # Função para gerar a URL do Google Calendar para a consulta
    def google_calendar_link(self):
        # Obtém a data e hora da consulta
        data_inicio = self.data_aberta.data.strftime('%Y%m%dT%H%M%SZ')
        data_fim = (self.data_aberta.data + timezone.timedelta(hours=1)).strftime('%Y%m%dT%H%M%SZ')  # duração de 1 hora

        # Parâmetros do evento
        titulo = f"Consulta com Dr. {self.medico.nome}"
        descricao = f"Consulta com o médico {self.medico.nome} e paciente {self.paciente.username}.\nLink do Google Meet: {self.link}"
        local = "Local da consulta"  # Você pode usar um campo adicional no modelo se quiser armazenar o local

        # Monta a URL para o Google Calendar
        return f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={titulo}&dates={data_inicio}/{data_fim}&details={descricao}&location={local}&sf=true&output=xml"


class Documento(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.DO_NOTHING)
    titulo = models.CharField(max_length=30)
    documento = models.FileField(upload_to='documentos')

    def __str__(self):
        return self.titulo