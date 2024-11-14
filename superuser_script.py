import os
import sys
import django
from django.core.management import call_command
from django.conf import settings

# Configuração do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings') 
django.setup()

# Importa o modelo de usuário após a configuração do Django
from django.contrib.auth import get_user_model

def create_superuser(username, email, password):
    try:
        # Chama o comando para criar um superuser
        User = get_user_model()
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f'Superuser {username} criado com sucesso!')
    except Exception as e:
        print(f'Erro ao criar superuser: {e}')

if __name__ == "__main__":
    superuser_username = 'admin'
    superuser_email = ''
    superuser_password = 'admin'

    create_superuser(superuser_username, superuser_email, superuser_password)
