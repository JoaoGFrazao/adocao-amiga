from django.test import TestCase
from adocao.tests.test_base import TestBase
from django.contrib.auth.models import User
from django.contrib import auth
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import authenticate


class TestViews(TestBase, APITestCase):
    def setUp(self):
        super().setUp()

    def test_animal_list(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get('/animais/')
        self.assertEqual(response.status_code, 200)

    def test_raca_list(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get('/racas/')
        self.assertEqual(response.status_code, 200)

    def test_tags_list(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get('/tags/')
        self.assertEqual(response.status_code, 200)

    def test_cores_pelagem_list(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get('/cores-pelagem/')
        self.assertEqual(response.status_code, 200)

    def test_tipos_pelo_list(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get('/tipos-pelo/')
        self.assertEqual(response.status_code, 200)

    def test_user_list(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get('/user/')
        self.assertEqual(response.status_code, 200)

    def test_galeria_animal_list(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get('/galeria-animal/')
        self.assertEqual(response.status_code, 200)

    def test_animal_galeria_list(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get('/animal-galeria/')
        self.assertEqual(response.status_code, 200)

    def test_animal_detail(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get('/um-animal/1/')
        self.assertEqual(response.status_code, 200)

    def test_user_profile_page(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get('/user-profile-page/1')
        self.assertEqual(response.status_code, 200)

    def test_animal_galeria_list(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get('/animal-galeria-filtro')
        self.assertEqual(response.status_code, 200)

    def test_animal_galeria_detail(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get('/um-galeria-animal/1/')
        data = response.json()
        first_item_id = data["results"][0]["id"]
        first_item_especie = data["results"][0]["especie"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["count"], 1)
        self.assertEqual(first_item_id, 1)
        self.assertEqual(first_item_especie, "Cachorro")

    def test_um_animal_datail(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get('/um-animal/1/')
        data = response.json()
        item_id = data["id"]
        item_especie = data["especie"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(item_id, 1)
        self.assertEqual(item_especie, "Cachorro")

    def test_user_animal_list(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get('/animal/1/user')
        data = response.json()
        item_id = data["results"][0]["id"]
        item_especie = data["results"][0]["especie"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(item_id, 1)
        self.assertEqual(item_especie, "Cachorro")

    def test_animal_filtro(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get('/animal-filtro?especie=cachorro&energia_min=3&energia_max=5&castrado=False&idade_min=2&idade_max=5')
        data = response.json()
        first_item_id = data["results"][0]["id"]
        first_item_especie = data["results"][0]["especie"]
        first_item_nome = data["results"][0]["nome"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["count"], 1)
        self.assertEqual(first_item_id, 1)
        self.assertEqual(first_item_especie, "Cachorro")
        self.assertEqual(first_item_nome, "Rex")