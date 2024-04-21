from django.contrib import admin
from .models import Especialidades, DadosMedico

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

admin.site.register(Especialidades, EspecialidadesAdmin)
admin.site.register(DadosMedico, DadosMedicoAdmin)