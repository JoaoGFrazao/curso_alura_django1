from django.contrib import admin
from apps.galeria.models import Fotografia


#Mostrando DB no admin e a classe dizendo como listar as entradas, onde clicar para acessar os itens e criou uma forma de pesquisar por entradas específicas
class ListandoFotografias(admin.ModelAdmin):
    list_display = ("id", "nome", "legenda", "publicada")
    list_display_links = ("id", "nome")
    search_fields = ("nome",)
    list_filter = ("categoria", "usuario")
    list_editable = ("publicada", )
    list_per_page = 10

admin.site.register(Fotografia, ListandoFotografias)

# Register your models here.
