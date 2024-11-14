import os
import django
from django.db import transaction

# Configuração do Django para permitir o uso do ORM
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from adocao.models import Raca, CorPelagem, TipoPelo, ESPECIE_CHOICES

cachorros = {
    "Labrador Retriever": {
        'cores': ['Caramelo', 'Preto', 'Marrom'],
        'tipos': ['Curto']
    },
    "Golden Retriever": {
        'cores': ['Caramelo'],
        'tipos': ['Longo']
    },
    "Bulldog Francês": {
        'cores': ['Branco', 'Preto', 'Branco e Preto', 'Dourado', 'Dourado e Branco', 'Preto e Dourado'],
        'tipos': ['Curto']
    },
    "Bulldog Inglês": {
        'cores': ['Dourado e Branco', 'Branco', 'Dourado', 'Malhado'],
        'tipos': ['Curto']
    },
    "Poodle": {
        'cores': ['Branco', 'Preto', 'Café', 'Cinza', 'Apricot'],
        'tipos': ['Cacheado', 'Encaracolado']
    },
    "Beagle": {
        'cores': ['Tricolor', 'Limão', 'Preto e Branco'],
        'tipos': ['Curto']
    },
    "Rottweiler": {
        'cores': ['Preto e Fogo'],
        'tipos': ['Curto']
    },
    "Yorkshire Terrier": {
        'cores': ['Azul e Dourado', 'Dourado'],
        'tipos': ['Longo']
    },
    "Boxer": {
        'cores': ['Fawn', 'Branco', 'Tigrado'],
        'tipos': ['Curto']
    },
    "Dachshund": {
        'cores': ['Vermelho', 'Preto e Fogo', 'Tigrado'],
        'tipos': ['Curto', 'Longo']
    },
    "Siberian Husky": {
        'cores': ['Preto e Branco', 'Cinza e Branco', 'Vermelho e Branco', 'Branco'],
        'tipos': ['Médio']
    },
    "Shih Tzu": {
        'cores': ['Dourado', 'Branco', 'Preto', 'Tigrado', 'Cinza', 'Chocolate'],
        'tipos': ['Longo']
    },
    "Doberman Pinscher": {
        'cores': ['Preto e Fogo', 'Chocolate e Fogo'],
        'tipos': ['Curto']
    },
    "Pembroke Welsh Corgi": {
        'cores': ['Vermelho', 'Tricolor', 'Sable', 'Branco'],
        'tipos': ['Curto']
    },
    "Australian Shepherd": {
        'cores': ['Merle', 'Preto', 'Red Merle', 'Sable', 'Branco'],
        'tipos': ['Médio']
    },
    "Chihuahua": {
        'cores': ['Fawn', 'Preto', 'Branco', 'Chocolate', 'Dourado'],
        'tipos': ['Curto', 'Longo']
    },
    "Great Dane": {
        'cores': ['Preto', 'Malhado', 'Branco', 'Fawn', 'Azul'],
        'tipos': ['Curto']
    },
    "Pug": {
        'cores': ['Preto', 'Bege'],
        'tipos': ['Curto']
    },
    "Boston Terrier": {
        'cores': ['Preto e Branco', 'Branco e Dourado'],
        'tipos': ['Curto']
    },
    "Havanese": {
        'cores': ['Branco', 'Preto', 'Chocolate', 'Dourado', 'Tigrado'],
        'tipos': ['Longo']
    },
    "Bichon Frise": {
        'cores': ['Branco'],
        'tipos': ['Cacheado']
    },
    "Saint Bernard": {
        'cores': ['Branco e Marrom', 'Marrom'],
        'tipos': ['Longo']
    },
    "Border Collie": {
        'cores': ['Preto e Branco', 'Tricolor', 'Marron e Branco'],
        'tipos': ['Médio']
    },
    "Shetland Sheepdog": {
        'cores': ['Sable', 'Tricolor', 'Preto e Branco'],
        'tipos': ['Longo']
    },
    "Cavalier King Charles Spaniel": {
        'cores': ['Blenheim', 'Tricolor', 'Ruby', 'Preto e Branco'],
        'tipos': ['Longo']
    },
    "Bull Terrier": {
        'cores': ['Branco', 'Preto', 'Tigrado', 'Malhado'],
        'tipos': ['Curto']
    },
    "Akita": {
        'cores': ['Branco', 'Dourado', 'Preto', 'Tigrado'],
        'tipos': ['Curto']
    },
    "Maltese": {
        'cores': ['Branco'],
        'tipos': ['Longo']
    },
    "Weimaraner": {
        'cores': ['Cinza', 'Cinza Prateado'],
        'tipos': ['Curto']
    },
    "German Shepherd": {
        'cores': ['Preto e Fogo', 'Sable', 'Branco'],
        'tipos': ['Curto']
    },
    "Cocker Spaniel": {
        'cores': ['Preto', 'Dourado', 'Marmoreado'],
        'tipos': ['Longo']
    },
    "American Pit Bull Terrier": {
        'cores': ['Preto', 'Branco', 'Tigrado', 'Dourado'],
        'tipos': ['Curto']
    },
    "English Springer Spaniel": {
        'cores': ['Tricolor', 'Preto e Branco', 'Chocolate e Branco'],
        'tipos': ['Longo']
    },
    "Bloodhound": {
        'cores': ['Verde e Marrom', 'Preto e Fogo'],
        'tipos': ['Curto']
    },
    "Alaskan Malamute": {
        'cores': ['Cinza e Branco', 'Preto e Branco', 'Vermelho e Branco'],
        'tipos': ['Médio']
    },
    "Newfoundland": {
        'cores': ['Preto', 'Marrom', 'Cinza'],
        'tipos': ['Longo']
    },
    "Irish Setter": {
        'cores': ['Vermelho', 'Dourado'],
        'tipos': ['Longo']
    },
    "Belgian Malinois": {
        'cores': ['Fawn', 'Preto'],
        'tipos': ['Curto']
    },
    "West Highland White Terrier": {
        'cores': ['Branco'],
        'tipos': ['Curto']
    },
    "Old English Sheepdog": {
        'cores': ['Cinza e Branco'],
        'tipos': ['Longo']
    },
    "Papillon": {
        'cores': ['Branco e Preto', 'Branco e Laranja'],
        'tipos': ['Longo']
    },
    "Scottish Terrier": {
        'cores': ['Preto', 'Branco', 'Dourado'],
        'tipos': ['Curto']
    },
    "American Bulldog": {
        'cores': ['Branco', 'Dourado', 'Preto e Branco'],
        'tipos': ['Curto']
    },
    "Basenji": {
        'cores': ['Tigrado', 'Preto e Branco', 'Vermelho'],
        'tipos': ['Curto']
    },
    "Airedale Terrier": {
        'cores': ['Preto e Castanho', 'Castanho'],
        'tipos': ['Curto']
    },
    "Shiba Inu": {
        'cores': ['Vermelho', 'Preto e Fogo', 'Sesame'],
        'tipos': ['Curto']
    },
    "Norwegian Elkhound": {
        'cores': ['Cinza', 'Preto', 'Dourado'],
        'tipos': ['Curto']
    },
    "Samoyed": {
        'cores': ['Branco'],
        'tipos': ['Longo']
    }
}


def adicionar_dados_cachorro():
    with transaction.atomic():
        for raca_nome, atributos in cachorros.items():
            raca, created = Raca.objects.get_or_create(nome=raca_nome.title(), especie='cachorro')
            
            for cor_nome in atributos['cores']:
                cor, created = CorPelagem.objects.get_or_create(nome=cor_nome)
                raca.cores_pelo_possiveis.add(cor)

            # Adiciona os tipos de pelo
            for tipo_nome in atributos['tipos']:
                tipo, created = TipoPelo.objects.get_or_create(nome=tipo_nome)
                raca.tipos_pelo_possiveis.add(tipo)

if __name__ == "__main__":
    adicionar_dados_cachorro()