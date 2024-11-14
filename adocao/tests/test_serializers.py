from adocao.serializers import *
from adocao.models import *
from django.test import TestCase
from adocao.tests.test_base import TestBase

class TestSerializer(TestBase):
    def setUp(self):
        super().setUp()
        self.serializer_raca = RacaSerializer(instance=Raca.objects.all().first())
        self.serializer_tag = TagSerializer(instance=Tag.objects.all().first())
        self.serializer_tipo_pelo = TipoPeloSerializer(instance=TipoPelo.objects.all().first())
        self.serializer_cor_pelagem = CorPelagemSerializer(instance=CorPelagem.objects.all().first())
        self.serializer_galeria_animal = GaleriaAnimalSerializer(instance=GaleriaAnimal.objects.all().first())
        self.serializer_galeria_animal_spec = GaleriaAnimalSpecSerializer(instance=GaleriaAnimal.objects.all().first())
        self.serializer_animal_usuario = AnimalUsuarioSerializer(instance=Animal.objects.all().first())
        self.serializer_animal = AnimalSerializer(instance=Animal.objects.all().first())
        self.serializer_animal_spec = AnimalSpecSerializer(instance=Animal.objects.all().first())
        self.serializer_animal_galeria = GaleriaAnimalSerializer(instance=GaleriaAnimal.objects.all().first())
        self.serilizer_user = UserSerializer(instance=User.objects.all().first())
        self.serializer_user_profile = UserProfileSerializer(instance=UserProfile.objects.all().first())
        self.serializer_user_profile_name = UserProfileNameSerializer(instance=UserProfile.objects.all().first())
        self.serializer_user_profile_page = UserProfilePageSerializer(instance=UserProfile.objects.all().first())

    def teste_verifica_campos_serializados_de_raca(self):
        dados = self.serializer_raca.data
        self.assertEqual(set(dados.keys()), set(['id', 'nome', 'especie', "tipos_pelo_possiveis", 'cores_pelo_possiveis']))

    def teste_verifica_campos_serializados_de_tag(self):
        dados = self.serializer_tag.data
        self.assertEqual(set(dados.keys()), set(['id', 'nome']))

    def teste_verifica_campos_serializados_de_tipo_pelo(self):
        dados = self.serializer_tipo_pelo.data
        self.assertEqual(set(dados.keys()), set(['id', 'nome', 'imagem']))

    def teste_verifica_campos_serializados_de_cor_pelagem(self):
        dados = self.serializer_cor_pelagem.data
        self.assertEqual(set(dados.keys()), set(['id', 'nome', 'imagem']))

    def teste_verifica_campos_serializados_de_galeria_animal(self):
        dados = self.serializer_galeria_animal.data
        self.assertEqual(set(dados.keys()), set(['id', 'especie', 'imagem']))

    def teste_verifica_campos_serializados_de_galeria_animal_spec(self):
        dados = self.serializer_galeria_animal_spec.data
        self.assertEqual(set(dados.keys()), set(['id', 'imagem']))

    def teste_verifica_campos_serializados_de_animal_usuario(self):
        dados = self.serializer_animal_usuario.data
        self.assertEqual(set(dados.keys()), set([
            'id', 'nome', 'especie', 'raca', 'tags', 'tipo_de_pelo', 'cor_padrao_pelagem',
             'fotos', 'tutor', 'data_nascimento', 'esta_para_adocao', 'foi_adotado', 'fiv', 'felv',
             'descricao', 'mostrar_no_perfil', 'sociavel_com_animais', 'castrado', 'energia', 'foi_adotado'
            ]))
        self.assertEqual(dados['tutor'], self.user_abrigo.id)

    def teste_verifica_campos_serializados_de_animal(self):
        dados = self.serializer_animal.data
        self.assertEqual(set(dados.keys()), set([
            'id', 'nome', 'especie', 'raca', 'tags', 'tipo_de_pelo', 'cor_padrao_pelagem',
             'fotos', 'tutor', 'data_nascimento', 'esta_para_adocao', 'foi_adotado', 'fiv', 'felv',
             'descricao', 'mostrar_no_perfil', 'sociavel_com_animais', 'castrado', 'energia', 'foi_adotado'
            ]))

    def teste_verifica_campos_serializados_de_animal_spec(self):
        dados = self.serializer_animal_spec.data
        self.assertEqual(set(dados.keys()), set(['id', 'tutor', 'especie', 'nome', 'raca', 'tags', 'tipo_de_pelo', 'cor_padrao_pelagem']))

    def teste_verifica_campos_serializados_de_animal_galeria(self):
        dados = self.serializer_animal_galeria.data
        self.assertEqual(set(dados.keys()), set(['id', 'imagem', 'especie']))

    def teste_verifica_campos_serializados_de_user(self):
        dados = self.serilizer_user.data
        self.assertEqual(set(dados.keys()), set(['id', 'username']))

    def teste_verifica_campos_serializados_de_user_profile(self):
        dados = self.serializer_user_profile.data
        self.assertEqual(set(dados.keys()), set(['id', 'user', 'tipo', 'primeiro_nome_ou_nome_abrigo', 'sobrenome', 'email',
                                                  'telefone_celular', 'foto_logo', 'cpf', 'cnpj', 'animais_em_casa', 'descricao', 'uf',
                                                  'endereco', 'buscando_oferecendo']))

    def teste_verifica_campos_serializados_de_user_profile_name(self):
        dados = self.serializer_user_profile_name.data
        self.assertEqual(set(dados.keys()), set(['user', 'primeiro_nome_ou_nome_abrigo']))