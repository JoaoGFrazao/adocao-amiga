import os
import django

# Configuração do Django para permitir o uso do ORM
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from adocao.models import Tag

tags = [
    'Carinhoso', 'Gosta de Colo', 'Gosta de Crianças', 'Brincalhão', 'Quieto', 'Medroso', 'Assustado', 'Late pouco', 'Adora passear', 'Gosta de ser Escovado'
    ]


def adicionar_tags():
    for tag in tags:
        Tag.objects.create(nome = tag)

if __name__ == "__main__":
    adicionar_tags()