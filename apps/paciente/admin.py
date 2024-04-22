from django.contrib import admin
from .models import Consulta, Documento

class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('id', 'paciente', 'data_aberta', 'status', 'link',)
    list_display_links = ('id', 'paciente',)
    list_filter = ('paciente', 'data_aberta', 'status')
    filter_horizontal = ()
    fieldsets = ()

class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'consulta', 'titulo', 'documento',)
    list_display_links = ('id', 'consulta',)
    list_filter = ('consulta', 'titulo',)
    filter_horizontal = ()
    fieldsets = ()

admin.site.register(Consulta, ConsultaAdmin)
admin.site.register(Documento, DocumentoAdmin)