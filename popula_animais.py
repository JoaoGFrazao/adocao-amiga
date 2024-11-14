import os
import django

# Configuração do Django para permitir o uso do ORM
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()
import random
from django.db.models import Q
from faker import Faker
from transliterate import translit
from datetime import datetime, timedelta
from adocao.models import Tag, Animal, Raca, TipoPelo, CorPelagem, ESPECIE_CHOICES, GaleriaAnimal, AnimalGaleria, UserProfile
from django.contrib.auth.models import User
from adocao.models import profile_por_user, raca_especie
fake = Faker("ru_RU")



def data_aleatoria():
    data_atual = datetime.now()
    dias_aleatorios = random.randint(0, 15 * 365)
    data_aleatoria = data_atual - timedelta(days=dias_aleatorios)
    return data_aleatoria

def adocao_tf(tutor):
    retorno = []
    if tutor == 'adotante' or tutor == 'Adotante':
        esta_para_adocao = False
        foi_adotado = random.choice([False, True, None])
        retorno.append(esta_para_adocao)
        retorno.append(foi_adotado)

    if tutor == 'Abrigo' or tutor == 'abrigo':
        esta_para_adocao = random.choice([True, False])
        retorno.append(esta_para_adocao)

        if esta_para_adocao == True:
            foi_adotado = False
            retorno.append(foi_adotado)
        if esta_para_adocao == False:
            foi_adotado = True
            retorno.append(foi_adotado)
    return retorno


def adiciona_animais(number):
    for i in range(number):
        nome_cirilico = fake.first_name()
        nome_latino = translit(nome_cirilico, 'ru', reversed=True)
        especie = random.choice(ESPECIE_CHOICES)[0]
        tutor = random.choice(User.objects.exclude(id = 1))
        tutor_tipo = profile_por_user(tutor.id)
        raca = random.choice([random.choice(raca_especie(especie)), None])
        esta_para_adocao = adocao_tf(tutor_tipo)[0]
        foi_adotado = adocao_tf(tutor_tipo)[1]
        animal = Animal.objects.create(
            tutor = tutor,
            nome = nome_latino,
            descricao = fake.text(),
            especie = especie,
            raca = raca,
            energia = random.randint(1, 5),
            tipo_de_pelo = random.choice(raca.tipos_pelo_possiveis.all()) if raca !=None else random.choice(TipoPelo.objects.all()),
            cor_padrao_pelagem = random.choice(raca.cores_pelo_possiveis.all()) if raca !=None else random.choice(CorPelagem.objects.all()),
            esta_para_adocao = esta_para_adocao,
            foi_adotado = foi_adotado,
            castrado = random.choice([True, False]),
            sociavel_com_animais = random.choice([True, False]),
            data_nascimento = data_aleatoria(),
            mostrar_no_perfil = True if tutor_tipo == 'abrigo' or tutor_tipo == 'Abrigo' else random.choice([True, False]),
            fiv = None if especie == ESPECIE_CHOICES[0] else random.choice([True, False]),
            felv = None if especie == ESPECIE_CHOICES[0] else random.choice([True, False])

        )
        numero_aleatorio_img = random.randint(2, 5)
        imagens = GaleriaAnimal.objects.filter(especie__iexact=especie)
        
        for i in range (numero_aleatorio_img):
            img_aleatoria = random.choice(imagens)
            AnimalGaleria.objects.create(animal=animal, galeria=img_aleatoria, isMain=True if i == 1 else False)



        numero_aleatorio = random.randint(1, 4)
        tags = []
        for i in range (numero_aleatorio):
            tag_aleatoria = random.choice(Tag.objects.all())
            if tag_aleatoria in tags:
                pass
            else:
                tags.append(tag_aleatoria)

        for tag in tags:
            animal.tags.add(tag)

    print("Deu certo!")

if __name__ == "__main__":
    adiciona_animais(400)
