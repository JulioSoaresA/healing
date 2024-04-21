from django.contrib import admin
from .models import Especialidades, DadosMedico, DatasAbertas

class EspecialidadesAdmin(admin.ModelAdmin):
    list_display = ('id', 'especialidade')
    list_display_links = ('id', 'especialidade',)
    list_filter = ('especialidade',)
    filter_horizontal = ()
    fieldsets = ()


class DadosMedicoAdmin(admin.ModelAdmin):
    list_display = ('id','crm', 'nome', 'especialidade',)
    list_display_links = ('id', 'crm', 'nome',)
    list_filter = ('crm', 'nome', 'especialidade',)
    filter_horizontal = ()
    fieldsets = ()


class DatasAbertasAdmin(admin.ModelAdmin):
    list_display = ('id', 'data', 'user', 'agendado')
    list_display_links = ('id', 'data', 'user', 'agendado')
    list_filter = ('data', 'user', 'agendado')
    filter_horizontal = ()
    fieldsets = ()

admin.site.register(Especialidades, EspecialidadesAdmin)
admin.site.register(DadosMedico, DadosMedicoAdmin)
admin.site.register(DatasAbertas, DatasAbertasAdmin)