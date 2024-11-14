import os
import django
from django.db import transaction
# Configuração do Django para permitir o uso do ORM
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from adocao.models import Raca, CorPelagem, TipoPelo, ESPECIE_CHOICES

gatos = {
    "Persa": {
        'cores': ['Branco', 'Cinza', 'Preto', 'Dourado', 'Tigrado'],
        'tipos': ['Longo']
    },
    "Maine Coon": {
        'cores': ['Preto', 'Azul', 'Tigrado', 'Dourado'],
        'tipos': ['Longo']
    },
    "Siamês": {
        'cores': ['Seal Point', 'Chocolate Point', 'Lilac Point', 'Blue Point'],
        'tipos': ['Curto']
    },
    "Bengal": {
        'cores': ['Marmoreado', 'Tigrado', 'Spotted'],
        'tipos': ['Curto']
    },
    "Ragdoll": {
        'cores': ['Seal', 'Blue', 'Chocolate', 'Lilac'],
        'tipos': ['Longo']
    },
    "British Shorthair": {
        'cores': ['Azul', 'Preto', 'Branco', 'Creme', 'Tigrado'],
        'tipos': ['Curto']
    },
    "Sphynx": {
        'cores': ['Branco', 'Preto', 'Dourado', 'Rosa'],
        'tipos': ['Sem pelo']
    },
    "Abissínio": {
        'cores': ['Ruddy', 'Rufus', 'Sorrel', 'Blue'],
        'tipos': ['Curto']
    },
    "Scottish Fold": {
        'cores': ['Branco', 'Preto', 'Dourado', 'Tigrado'],
        'tipos': ['Curto', 'Longo']
    },
    "Burmese": {
        'cores': ['Sable', 'Champagne', 'Blue', 'Platinum'],
        'tipos': ['Curto']
    },
    "Norueguês da Floresta": {
        'cores': ['Branco', 'Cinza', 'Preto', 'Dourado'],
        'tipos': ['Longo']
    },
    "Devon Rex": {
        'cores': ['Preto', 'Chocolate', 'Dourado', 'Tigrado'],
        'tipos': ['Curto']
    },
    "Cornish Rex": {
        'cores': ['Branco', 'Preto', 'Cinza', 'Dourado'],
        'tipos': ['Curto']
    },
    "Tonquin": {
        'cores': ['Cinnamom', 'Chocolate', 'Lilac'],
        'tipos': ['Curto']
    },
    "Angorá Turco": {
        'cores': ['Branco', 'Preto', 'Dourado', 'Tigrado'],
        'tipos': ['Longo']
    },
    "Birmanês": {
        'cores': ['Blue', 'Seal', 'Chocolate', 'Lilac'],
        'tipos': ['Longo']
    },
    "Oriental Shorthair": {
        'cores': ['Branco', 'Preto', 'Cinza', 'Rosa'],
        'tipos': ['Curto']
    },
    "Selkirk Rex": {
        'cores': ['Branco', 'Preto', 'Dourado', 'Tigrado'],
        'tipos': ['Cacheado']
    },
    "Chartreux": {
        'cores': ['Azul', 'Cinza'],
        'tipos': ['Curto']
    },
    "American Shorthair": {
        'cores': ['Preto', 'Branco', 'Dourado', 'Tigrado'],
        'tipos': ['Curto']
    },
    "Ragamuffin": {
        'cores': ['Branco', 'Azul', 'Preto', 'Dourado'],
        'tipos': ['Longo']
    },
    "Balinês": {
        'cores': ['Blue', 'Seal', 'Chocolate'],
        'tipos': ['Longo']
    },
    "Somali": {
        'cores': ['Ruddy', 'Red', 'Blue', 'Fawn'],
        'tipos': ['Curto']
    },
    "Havana Brown": {
        'cores': ['Chocolate'],
        'tipos': ['Curto']
    },
    "Manx": {
        'cores': ['Preto', 'Branco', 'Dourado', 'Tigrado'],
        'tipos': ['Curto']
    },
    "Japanese Bobtail": {
        'cores': ['Branco', 'Preto', 'Dourado', 'Tigrado'],
        'tipos': ['Curto']
    },
    "Egyptian Mau": {
        'cores': ['Prata', 'Dourado', 'Bronze'],
        'tipos': ['Curto']
    },
    "Turkish Van": {
        'cores': ['Branco com manchas coloridas'],
        'tipos': ['Longo']
    },
    "LaPerm": {
        'cores': ['Branco', 'Preto', 'Tigrado', 'Dourado'],
        'tipos': ['Cacheado']
    },
    "Scottish Straight": {
        'cores': ['Branco', 'Preto', 'Dourado', 'Tigrado'],
        'tipos': ['Curto', 'Longo']
    },
    "Russian Blue": {
        'cores': ['Azul'],
        'tipos': ['Curto']
    },
    "Bengal": {
        'cores': ['Marmoreado', 'Spotted', 'Tigrado'],
        'tipos': ['Curto']
    },
    "Tuxedo": {
        'cores': ['Preto e Branco'],
        'tipos': ['Curto']
    },
    "Munchkin": {
        'cores': ['Preto', 'Branco', 'Dourado', 'Tigrado'],
        'tipos': ['Curto', 'Longo']
    },
    "Burmese": {
        'cores': ['Sable', 'Champagne', 'Blue', 'Platinum'],
        'tipos': ['Curto']
    },
    "American Curl": {
        'cores': ['Branco', 'Preto', 'Dourado', 'Tigrado'],
        'tipos': ['Curto', 'Longo']
    },
    "Ragdoll": {
        'cores': ['Seal', 'Blue', 'Chocolate', 'Lilac'],
        'tipos': ['Longo']
    },
    "Sagrado da Birmânia": {
        'cores': ['Branco com pontos coloridos'],
        'tipos': ['Longo']
    },
    "Exotic Shorthair": {
        'cores': ['Branco', 'Preto', 'Dourado', 'Tigrado'],
        'tipos': ['Curto']
    },
    "Siamês de ponta": {
        'cores': ['Seal Point', 'Chocolate Point', 'Blue Point'],
        'tipos': ['Curto']
    },
    "Nebelung": {
        'cores': ['Azul'],
        'tipos': ['Longo']
    },
    "Snowshoe": {
        'cores': ['Branco e Tigrado'],
        'tipos': ['Curto']
    },
    "Coon de Maine": {
        'cores': ['Preto', 'Branco', 'Dourado', 'Tigrado'],
        'tipos': ['Longo']
    },
    "Birman": {
        'cores': ['Seal', 'Blue', 'Chocolate', 'Lilac'],
        'tipos': ['Longo']
    },
    "Siberian": {
        'cores': ['Branco', 'Cinza', 'Preto', 'Dourado'],
        'tipos': ['Longo']
    },
    "Balinês": {
        'cores': ['Seal', 'Chocolate', 'Blue', 'Lilac'],
        'tipos': ['Longo']
    },
    "Donskoy": {
        'cores': ['Branco', 'Preto', 'Dourado', 'Tigrado'],
        'tipos': ['Sem pelo']
    },
    "Serama": {
        'cores': ['Variadas'],
        'tipos': ['Sem pelo', 'Curto']
    },
    "LaPerm": {
        'cores': ['Branco', 'Preto', 'Tigrado', 'Dourado'],
        'tipos': ['Cacheado']
    },
    "Toyger": {
        'cores': ['Tigrado', 'Laranja', 'Preto'],
        'tipos': ['Curto']
    }
}

def adicionar_dados_gatos():
    with transaction.atomic():
        for raca_nome, atributos in gatos.items():
            raca = Raca.objects.create(nome=raca_nome, especie='gato')

            for cor_nome in atributos['cores']:
                cor, created = CorPelagem.objects.get_or_create(nome=cor_nome)
                raca.cores_pelo_possiveis.add(cor)

            for tipo_nome in atributos['tipos']:
                tipo, created = TipoPelo.objects.get_or_create(nome=tipo_nome)
                raca.tipos_pelo_possiveis.add(tipo)

if __name__ == "__main__":
    adicionar_dados_gatos()