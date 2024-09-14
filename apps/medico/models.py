from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

class Especialidades(models.Model):
    especialidade = models.CharField(max_length=100)
    icone = models.ImageField(upload_to="icones", null=True, blank=True)
    def __str__(self):
        return self.especialidade


class DadosMedico(models.Model):
    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'prefiro não dizer')
    )
    crm = models.CharField(max_length=30)
    nome = models.CharField(max_length=100)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    cep = models.CharField(max_length=15)
    rua = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    numero = models.IntegerField()
    rg = models.ImageField(upload_to="rgs")
    cedula_identidade_medica = models.ImageField(upload_to='cim')
    foto = models.ImageField(upload_to="fotos_perfil")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    descricao = models.TextField(null=True, blank=True)
    especialidade = models.ForeignKey(Especialidades, on_delete=models.DO_NOTHING, null=True, blank=True)
    valor_consulta = models.FloatField(default=100)
    def __str__(self):
        return self.nome

    @property
    def proxima_data(self):
        return DatasAbertas.objects.filter(user=self.user, data__gte=datetime.now(), agendado=False).order_by('data').first()


class DatasAbertas(models.Model):
    data = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    agendado = models.BooleanField(default=False)

    def __str__(self):
        return str(self.data)

    def data_formatada(self):
        return self.data.strftime('%d/%m/%Y %H:%M')
    
    def dias_ate_data(self):
        # Obtém a data atual (apenas a parte da data, sem a hora)
        hoje = timezone.now().date()

        # Obtém a data cadastrada (sem a hora)
        data_cadastrada = self.data.date()

        # Calcula a diferença em dias
        diferenca = (data_cadastrada - hoje).days
        
        if diferenca == 0:
            return 'Hoje'
        elif diferenca == 1:
            return f'em {diferenca} dia'
        elif diferenca < 0:
            return 'Data passada'
        else:
            return f'em {diferenca} dias'