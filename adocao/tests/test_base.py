from django.test import TestCase
from adocao.models import Raca, TipoPelo, CorPelagem, GaleriaAnimal, Tag, Animal, UserProfile, UF_CHOICES
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from validate_docbr import CNPJ, CPF
import faker
import random
from popula_cachorro import adicionar_dados_cachorro, cachorros
from popula_gato import adicionar_dados_gatos, gatos
from popula_tags import adicionar_tags, tags

class TestBase(TestCase):
    def setUp(self):
        fake = faker.Faker('pt_BR')
        self.user_abrigo = User.objects.create_user(username='testuser-abrigo', password='12345')
        self.user_profile_abrigo = UserProfile.objects.create(
            user=self.user_abrigo,
            primeiro_nome_ou_nome_abrigo='Teste_Abrigo',
            sobrenome=None,
            cpf=None,
            cnpj=CNPJ().generate(),
            email = 'teste_abrigo@gmail.com',
            telefone_celular=21999999999,
            endereco=fake.address(),
            uf=random.choice(UF_CHOICES)[0],
            tipo='abrigo',
            descricao=fake.text(),
            animais_em_casa=None,
            buscando_oferecendo ="Ambos",
            )
        self.superuser = User.objects.create_superuser(username='admin', password='admin')
        self.user_adotante = User.objects.create_user(username='testuser-adotante', password='67890')
        self.user_profile_adotante = UserProfile.objects.create(
            user=self.user_adotante,
            primeiro_nome_ou_nome_abrigo='Teste',
            sobrenome="de Adotante",
            cpf=CPF().generate(),
            cnpj=None,
            email = 'teste_adotante@gmail.com',
            telefone_celular=21988888888,
            endereco=fake.address(),
            uf=random.choice(UF_CHOICES)[0],
            tipo='adotante',
            descricao=fake.text(),
            animais_em_casa=True,
            buscando_oferecendo ="Gatos",
            )
        
        adicionar_tags()
        adicionar_dados_cachorro()
        adicionar_dados_gatos()

        self.galeria_animal_c1 = GaleriaAnimal.objects.create(
            especie='Cachorro',
            imagem='/dog.4501.jpg',

        )
        self.galeria_animal_c2 = GaleriaAnimal.objects.create(
            especie='Cachorro',
            imagem='/dog.4502.jpg'
        )
        self.galeria_animal_c3 = GaleriaAnimal.objects.create(
            especie='Cachorro',
            imagem='/dog.4503.jpg'
        )

        self.galeria_animal_g1 = GaleriaAnimal.objects.create(
            especie='Gato',
            imagem='/cat.4501.jpg'
        )
        self.galeria_animal_g2 = GaleriaAnimal.objects.create(
            especie='Gato',
            imagem='/cat.4502.jpg'
        )
        self.galeria_animal_g3 = GaleriaAnimal.objects.create(
            especie='Gato',
            imagem='/cat.4503.jpg'
        )

        self.animal_c1 = Animal.objects.create(
            tutor=self.user_abrigo,
            especie='Cachorro',
            raca=get_object_or_404(Raca, nome='Labrador Retriever'),
            tipo_de_pelo=get_object_or_404(TipoPelo, nome='Curto'),
            cor_padrao_pelagem=get_object_or_404(CorPelagem, nome='Caramelo'),
            nome='Rex',
            descricao='Cachorro muito amigável',
            energia=4,
            esta_para_adocao=True,
            foi_adotado=False,
            castrado=False,
            fiv=None,
            felv=None,
            data_nascimento='2021-10-20',
            sociavel_com_animais=True
        )
        self.animal_c1.tags.add(get_object_or_404(Tag, nome='Medroso'))
        self.animal_c1.fotos.add(self.galeria_animal_c1, self.galeria_animal_c2, self.galeria_animal_c3)

        self.animal_g1 = Animal.objects.create(
            tutor=self.user_adotante,
            especie='Gato',
            raca=get_object_or_404(Raca, nome='Ragdoll'),
            tipo_de_pelo=get_object_or_404(TipoPelo, nome='Longo'),
            cor_padrao_pelagem=get_object_or_404(CorPelagem, nome='Blue'),
            nome='Lyudmila',
            descricao='Gata muito amigável',
            energia=2,
            esta_para_adocao=False,
            foi_adotado=None,
            castrado=False,
            fiv=False,
            felv=False,
            data_nascimento='2021-10-20',
            sociavel_com_animais=True
        )
        self.animal_g1.tags.add(get_object_or_404(Tag, nome='Carinhoso'))
        self.animal_g1.fotos.add(self.galeria_animal_g1, self.galeria_animal_g2, self.galeria_animal_g3)