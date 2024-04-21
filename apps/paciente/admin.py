from django.contrib import admin
from .models import Consulta

class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('id', 'paciente', 'data_aberta', 'status', 'link',)
    list_display_links = ('id', 'paciente',)
    list_filter = ('paciente', 'data_aberta', 'status')
    filter_horizontal = ()
    fieldsets = ()

admin.site.register(Consulta, ConsultaAdmin)