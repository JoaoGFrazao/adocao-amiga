import os
import django
from django.db import transaction

# Configuração do Django para permitir o uso do ORM
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from adocao.models import GaleriaAnimal
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

imagens_cachorros = 'dogs'
lista_imagens_cachorros = []

for arquivo in os.listdir(imagens_cachorros):
    if any(arquivo.lower().endswith(ext) for ext in 'jpg'):
        lista_imagens_cachorros.append(arquivo)

imagens_gatos = 'cats'
lista_imagens_gatos = []

for arquivo in os.listdir(imagens_gatos):
    if any(arquivo.lower().endswith(ext) for ext in 'jpg'):
        lista_imagens_gatos.append(arquivo)


def adiciona_fotos():
    for arquivo_nome in lista_imagens_cachorros:
        caminho_imagem = os.path.join(imagens_cachorros, arquivo_nome)

        with open(caminho_imagem, 'rb') as img:
            galeria_animal = GaleriaAnimal(imagem=File(img, name=arquivo_nome), especie = 'cachorro')
            galeria_animal.save()

    for arquivo_nome in lista_imagens_gatos:
        caminho_imagem = os.path.join(imagens_gatos, arquivo_nome)

        with open(caminho_imagem, 'rb') as img:
            galeria_animal = GaleriaAnimal(imagem=File(img, name=arquivo_nome), especie = 'gato')
            galeria_animal.save()
    


if __name__ == "__main__":
    adiciona_fotos()