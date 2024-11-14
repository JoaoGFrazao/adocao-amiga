from django.shortcuts import render
from django.db.models import Q
from adocao.serializers import *
from rest_framework import viewsets, generics, filters, status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime
from dateutil.relativedelta import relativedelta
from rest_framework.response import Response
from django.contrib.auth.models import User
from adocao.models import Tag, Animal, Raca, TipoPelo, CorPelagem, ESPECIE_CHOICES, ENERGIA_CHOICES, UserProfile
from adocao.throttles import *

#ViewSets padrões para ver todos os dados de cada tabela
class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all().order_by('id')
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["nome", "=id"]
    ordering_fields = ['nome']
    http_method_names = [ 'get', 'post']
    serializer_class = AnimalSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

class RacaViewSet(viewsets.ModelViewSet):
    queryset = Raca.objects.all().order_by('id')
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["nome", "=id"]
    ordering_fields = ['nome']
    http_method_names = [ 'get', 'post']
    serializer_class = RacaSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["nome", "=id"]
    ordering_fields = ['nome']
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    serializer_class = TagSerializer

class CorPelagemViewSet(viewsets.ModelViewSet):
    queryset = CorPelagem.objects.all().order_by('id')
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["nome", "=id"]
    ordering_fields = ['nome']
    http_method_names = [ 'get', 'post']
    serializer_class = CorPelagemSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

class TipoPeloViewSet(viewsets.ModelViewSet):
    queryset = TipoPelo.objects.all().order_by('id')
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["id", "tipo_id", "raca_id"]
    ordering_fields = ['id']
    http_method_names = [ 'get', 'post']
    serializer_class = TipoPeloSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

class GaleriaAnimalViewSet(viewsets.ModelViewSet):
    queryset = GaleriaAnimal.objects.all().order_by('id')
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["id", "imagem", "especie"]
    ordering_fields = ['id']
    http_method_names = [ 'get', 'post']
    serializer_class = GaleriaAnimalSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

class AnimalGaleriaViewSet(viewsets.ModelViewSet):
    queryset = AnimalGaleria.objects.all().order_by('id')
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["id", "animal", "galeria", "isMain"]
    ordering_fields = ['id']
    http_method_names = [ 'get', 'post']
    serializer_class = AnimalGaleriaSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

#ViewSets Genéricos
#_______ Views para detalhes de itens especificos
class UmGaleriaAnimal(generics.ListAPIView):
    serializer_class = GaleriaAnimalSerializer
    throttle_classes = [DetailUserRateThrottle, DetailAnonRateThrottle]
    http_method_names = [ 'get', 'post', 'put', 'delete']
    def get_queryset(self):
        id = self.kwargs['pk']
        q = GaleriaAnimal.objects.filter(pk = id).order_by('id')
        return q
    
class UmAnimalViewSet(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        id = self.kwargs['pk']
        q = Animal.objects.filter(pk = id).order_by('id')
        return q
    
    throttle_classes = [DetailUserRateThrottle, DetailAnonRateThrottle]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["nome", "=id"]
    ordering_fields = ['nome']
    http_method_names = [ 'get', 'put', 'delete']
    serializer_class = AnimalSerializer

class AnimalGaleriaFiltro(generics.ListAPIView):
    def get_queryset(self):
        id_animal = self.request.GET.get('id-animal')
        id_galeria = self.request.GET.get('id-galeria')
        q = AnimalGaleria.objects.filter()

        if id_animal == "None" or id_animal == None:
            id_animal = None
        else:
            id_animal = int(id_animal)

        if id_galeria == "None" or id_galeria == None:
            id_galeria = None
        else:
            id_galeria = int(id_galeria)

        if id_animal != None or id_galeria !=None:
            if id_animal != None:
                q = q.filter(animal = id_animal) 
            if id_galeria != None:
                q = q.filter(galeria = id_galeria)

        return q
    throttle_classes = [FilterUserRateThrottle, FilterAnonRateThrottle]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["id", "animal", "galeria", "isMain"]
    ordering_fields = ['id']
    http_method_names = ['get', 'put', 'delete']
    serializer_class = AnimalGaleriaSerializer
    
#______ Outras views genéricas
class UsuarioAnimais(generics.ListCreateAPIView):
    serializer_class = AnimalUsuarioSerializer
    http_method_names = [ 'get']
    throttle_classes = [FilterUserRateThrottle, FilterAnonRateThrottle]


    def get_queryset(self):
        user_pk = self.kwargs['user_pk']
        animais_usuario = Animal.objects.filter(tutor_id = user_pk)
        return animais_usuario

class AnimaisFilter(generics.ListAPIView):
    serializer_class = AnimalSerializer
    http_method_names = [ 'get']
    throttle_classes = [FilterUserRateThrottle, FilterAnonRateThrottle]
    def get_queryset(self):
        q = Animal.objects.filter(Q(mostrar_no_perfil = True) | Q(tutor = self.request.user)).order_by('id')
        if self.request.content_type == 'application/json':
            especie = self.request.data.get('especie', None)
            raca_id = self.request.data.get('raca', None)
            tipo_id = self.request.data.get('tipo_pelo', None)
            cor_id = self.request.data.get('cor_pelo', None)
            nome = self.request.data.get('sem_nome', None)   
            max_energia = self.request.data.get('energia_max', 5)
            min_energia = self.request.data.get('energia_min', 1)
            castrado = self.request.data.get('castrado', None)   
            fiv = self.request.data.get('fiv', None)   
            felv = self.request.data.get('felv', None)
            sociavel_com_animais = self.request.data.get('sociavel', None)
            idade_min = self.request.data.get('idade_min', 0)
            idade_max = self.request.data.get('idade_max', 50)
            user = self.request.data.get('user', None)
            esta_para_adocao = self.request.data.get('para_adocao', None)
        else:
            especie = self.request.GET.get('especie')
            raca_id = self.request.GET.get('raca')
            tipo_id = self.request.GET.get('tipo_pelo')
            cor_id = self.request.GET.get('cor_pelo')
            nome = self.request.GET.get('sem_nome')
            max_energia = self.request.GET.get('energia_max')
            min_energia = self.request.GET.get('energia_min')
            castrado = self.request.GET.get('castrado')
            fiv = self.request.GET.get('fiv')
            felv = self.request.GET.get('felv')
            sociavel_com_animais = self.request.GET.get('sca')
            idade_min = self.request.GET.get('idade_min')
            idade_max = self.request.GET.get('idade_max')
            user = self.request.GET.get('user')
            esta_para_adocao = self.request.GET.get('para_adocao')

        bool = [castrado, fiv, felv, sociavel_com_animais, nome, esta_para_adocao]
        mapeamento = {"True": True, "False": False, "None": None}
        bool_conv = [mapeamento.get(item, item) for item in bool]
        castrado = bool_conv[0]
        fiv = bool_conv[1]
        felv = bool_conv[2]
        sociavel_com_animais = bool_conv[3]
        nome = bool_conv[4]
        esta_para_adocao = bool_conv[5]

        inteiros = [raca_id, tipo_id, cor_id, max_energia, min_energia, idade_min, idade_max, user]
        inteiros_conv = []
        for i in inteiros:
            if i != "None" and i != None:
                i = int(i)
                inteiros_conv.append(i)
            else:
                i = None
                inteiros_conv.append(i)
        
        raca_id = inteiros_conv[0]
        tipo_id = inteiros_conv[1]
        cor_id = inteiros_conv[2]
        max_energia = inteiros_conv[3]
        min_energia = inteiros_conv[4]
        idade_min = inteiros_conv[5]
        idade_max = inteiros_conv[6]
        user = inteiros_conv[7]

        if esta_para_adocao == True:
            q = q.filter(esta_para_adocao = True)

        if user != None:
            q = q.filter(tutor__id = user)

        if castrado != None:
            q = q.filter(castrado=castrado)
        if sociavel_com_animais != None:
            q = q.filter(sociavel_com_animais = sociavel_com_animais)

        if especie != None:
            if especie in ESPECIE_CHOICES[0]:
                q = q.filter(Q(especie = 'cachorro') | Q(especie = 'Cachorro'))

            if especie in ESPECIE_CHOICES[1]:
                q = q.filter(Q(especie = 'gato') | Q(especie = 'Gato'))
                if fiv != None:
                    q = q.filter(fiv = fiv)
                if felv != None:
                    q = q.filter(felv = felv)

        if raca_id != None:
            q = q.filter(raca = raca_id)
        if cor_id != None:
            q = q.filter(cor_padrao_pelagem = cor_id)
        if tipo_id != None:
            q = q.filter(tipo_de_pelo = tipo_id)
        if nome != None:
            q = q.filter(nome__isnull = nome)

        if max_energia != None or min_energia != None:
            if max_energia !=None and min_energia == None:
                q = q.filter(energia__lte = max_energia)
            if max_energia == None and min_energia != None:
                q = q.filter(energia__gte = max_energia)
            if max_energia != None and min_energia != None:
                q = q.filter(energia__range = (min_energia, max_energia))
            else:
                raise ValidationError("os números de energia precisam estar entre 1 e 5")
        
        if idade_max != None or idade_min != None:
            data_atual = datetime.now().date()
            if idade_max != None and idade_min == None:
               nascimento = data_atual - relativedelta(years = idade_max)
               q = q.filter(data_nascimento__gte = nascimento)

            if idade_max == None and idade_min != None:
                nascimento = data_atual - relativedelta(years = idade_min)
                q = q.filter(data_nascimento__lte = nascimento)

            if idade_max != None and idade_min != None:
                nascimento_max = data_atual - relativedelta(years = idade_min)
                nascimento_min = data_atual - relativedelta(years = idade_max)
                q = q.filter(data_nascimento__range=(nascimento_min, nascimento_max))

        return q

#Views de User

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all().order_by('id')
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["id", "user_id", "primeiro_nome_ou_nome_abrigo"]
    ordering_fields = ['id']
    http_method_names = [ 'get', 'post']
    serializer_class = UserProfileSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

class UmUserProfileViewSet(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        id = self.kwargs['pk']
        q = UserProfile.objects.filter(pk = id).order_by('id')
        return q
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["id", "primeiro_nome_ou_nome_abrigo", 'tipo']
    ordering_fields = ['id']
    http_method_names = [ 'get', 'post', 'put', 'delete']
    serializer_class = UserProfileSerializer
    throttle_classes = [DetailUserRateThrottle, DetailAnonRateThrottle]

class UmUserProfilePageViewSet(generics.ListAPIView):
    def get_queryset(self):
        id = self.kwargs['pk']
        q = User.objects.filter(pk = id)
        return q
    http_method_names = [ 'get']
    serializer_class = UserProfilePageSerializer
    throttle_classes = [DetailUserRateThrottle, DetailAnonRateThrottle]

