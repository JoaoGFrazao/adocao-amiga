from django.contrib import admin
from adocao.models import Animal, Raca, TipoPelo, CorPelagem, Tag, GaleriaAnimal, AnimalGaleria, UserProfile
from django.utils.html import format_html


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'tipo', 'primeiro_nome_ou_nome_abrigo', 'uf']
    search_fields = ['id', 'primeiro_nome_ou_nome_abrigo', 'tipo']
    list_display_links = ['id', 'primeiro_nome_ou_nome_abrigo', 'uf', 'tipo']


class AnimalGaleriaInline(admin.TabularInline):
    model = AnimalGaleria
    extra = 1  # Número de linhas extras para criar novos registros
    fields = ('galeria', 'isMain')  # Campos que você quer exibir
    autocomplete_fields = ['galeria']  # Isso permite selecionar GaleriaAnimal com o autocompletar

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'especie', 'raca', 'energia', 'esta_para_adocao', 'foi_adotado', 'castrado')
    list_filter = ('especie', 'raca', 'castrado', 'esta_para_adocao', 'foi_adotado')
    search_fields = ('nome', 'descricao')
    inlines = [AnimalGaleriaInline]

@admin.register(Raca)
class RacaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'especie')
    list_filter = ('especie',)
    search_fields = ('nome',)

@admin.register(TipoPelo)
class TipoPeloAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(CorPelagem)
class CorPelagemAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    list_display_links = ('id', 'nome')

@admin.register(GaleriaAnimal)
class GaleriaAnimalAdmin(admin.ModelAdmin):
    list_display = ('id', )
    list_display_links = ('id', )
    search_fields = ('id', )
