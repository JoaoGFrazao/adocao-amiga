import random
import faker
import os
import django
from validate_docbr import CPF, CNPJ

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from django.contrib.auth.models import User
from adocao.models import UserProfile, UF_CHOICES

fake = faker.Faker('pt_BR')

tipos = ['abrigo', 'adotante']
buscando_oferecendo_options = ['buscando', 'oferecendo']
buscando_opcoes_options = ['cachorro', 'gato', 'ambos']

def criar_usuarios(number):
    for i in range(number):  # Criar usuários fictícios
        # Cria um usuário
        username = fake.user_name()
        password = fake.password()
        user = User.objects.create_user(username=username, password=password)
        with open('usuarios_teste.txt', 'a') as arquivo:
            arquivo.write(f"\n usuario: {username} \n senha: {password}\n")
        print(f"\n usuario: {username} \n senha: {password}\n")

        # Cria um perfil de usuário
        tipo = random.choice(tipos)
        uf = random.choice(UF_CHOICES)[0]
        primeiro_nome = fake.first_name()
        abrigo_nome = fake.company()
        user_profile = UserProfile.objects.create(
            user=user,
            primeiro_nome_ou_nome_abrigo=primeiro_nome if tipo == 'adotante' else abrigo_nome,
            sobrenome=fake.last_name() if tipo == 'adotante' else None,
            cpf=CPF().generate() if tipo == 'adotante' else None,
            cnpj=CNPJ().generate() if tipo == 'abrigo' else None,
            email = '{}@{}'.format(primeiro_nome.lower(),fake.free_email_domain()) if tipo == 'adotante' else '{}@{}'.format(abrigo_nome.lower(),fake.free_email_domain()),
            telefone_celular=fake.phone_number() if tipo == 'abrigo' else None,
            endereco=fake.address(),
            uf=uf,
            tipo=tipo,
            descricao=fake.text() if tipo == 'abrigo' else None,
            animais_em_casa=random.choice([True, False]),
            buscando_oferecendo=random.choice(buscando_oferecendo_options),
        )
        user_profile.save()

if __name__ == "__main__":
    criar_usuarios(100)