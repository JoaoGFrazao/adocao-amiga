from adocao.models import Raca, TipoPelo, CorPelagem, GaleriaAnimal, Tag, Animal, UserProfile, UF_CHOICES
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from adocao.tests.test_base import TestBase
from validate_docbr import CPF



class TestModelsAnimal(TestBase):
    def setUp(self):
        super().setUp()

    def test_raca(self):
        self.assertEqual(self.animal_c1.raca.nome, 'Labrador Retriever')
        self.assertEqual(self.animal_c1.raca.especie.capitalize(), 'Cachorro')

    def test_animal(self):
        self.assertEqual(str(self.animal_c1), 'Rex')

    def test_animal_clean(self):
        self.assertIsNone(self.animal_c1.fiv)
        self.assertIsNone(self.animal_c1.felv)

    def test_animal_invalid_fiv_felv(self):
        self.animal_g1.fiv = None
        self.animal_g1.felv = None
        with self.assertRaises(ValidationError):
            self.animal_c1.clean()
        
    def test_dog_fiv_felv(self):
        self.animal_c1.fiv = False
        self.animal_c1.felv = False
        with self.assertRaises(ValidationError):
            self.animal_c1.clean()

    def test_animal_invalid_raca_especie(self):
        self.animal_c1.raca = Raca.objects.filter(especie = 'gato').first()
        with self.assertRaises(ValidationError):
            self.animal_c1.clean()
    
    def test_animal_sem_raca(self):
        self.animal_c1.raca = None
        try:
            self.animal_c1.clean()
        except ValidationError:
            self.fail("ValidationError foi gerado inesperadamente")

    def test_animal_invalid_adoption_status(self):
        self.animal_c1.esta_para_adocao = True
        self.animal_c1.foi_adotado = True
        with self.assertRaises(ValidationError):
            self.animal_c1.clean()

    def test_animal_invalid_profile(self):
        self.user_profile_abrigo.tipo = 'Adotante'
        self.user_profile_abrigo.save()
        self.animal_c1.esta_para_adocao = True
        with self.assertRaises(ValidationError):
            self.animal_c1.clean()

    def test_energia_range_min(self):
        self.animal_c1.energia = 0
        with self.assertRaises(ValidationError):
            self.animal_c1.clean()

    def test_energia_range_max(self):
        self.animal_c1.energia = 6
        with self.assertRaises(ValidationError):
            self.animal_c1.clean()
    

    
class TestModelsUser(TestBase):
    def setUp(self):
        super().setUp()
    
    def test_abrigo_attrs(self):
        self.user_profile_abrigo.telefone_celular = None
        with self.assertRaises(ValidationError):
            self.user_profile_abrigo.clean()

        self.user_profile_abrigo.descricao = ''
        with self.assertRaises(ValidationError):
            self.user_profile_abrigo.clean()

        self.user_profile_abrigo.uf = None
        with self.assertRaises(ValidationError):
            self.user_profile_abrigo.clean()
    
    def test_abrigo_attrs_clean(self):
        self.user_profile_abrigo.cpf = CPF().generate()
        self.user_profile_abrigo.sobrenome = 'Teste'
        self.user_profile_abrigo.clean()
        self.assertIsNone(self.user_profile_abrigo.cpf)
        self.assertIsNone(self.user_profile_abrigo.sobrenome)


class TestModelsCaracteristicas(TestBase):
    def setUp(self):
        super().setUp()

    def test_galeria_animal(self):
        self.assertEqual(self.galeria_animal_c1.especie, 'Cachorro')

    def test_tag(self):
        self.assertEqual(self.animal_c1.tags.all()[0].nome, 'Medroso')

    def test_tipo_pelo(self):
        self.assertEqual(self.animal_c1.tipo_de_pelo.nome, 'Curto')

    def test_cor_pelagem(self):
        self.assertEqual(self.animal_c1.cor_padrao_pelagem.nome, 'Caramelo')