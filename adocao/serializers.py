from rest_framework import serializers
from django.contrib.auth.models import User
from adocao.models import Tag, Animal, Raca, TipoPelo, CorPelagem, GaleriaAnimal, AnimalGaleria, ESPECIE_CHOICES, UserProfile

#Serializadores padrão para mostrar todos os dados de todas as tabelas

class RacaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raca
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class CorPelagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorPelagem
        fields = '__all__'

class TipoPeloSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPelo
        fields = '__all__'

class GaleriaAnimalSerializer(serializers.ModelSerializer):
    imagem = serializers.ImageField()
    class Meta:
        model = GaleriaAnimal
        fields = '__all__'

class GaleriaAnimalSpecSerializer(serializers.ModelSerializer):
    imagem = serializers.ImageField()
    class Meta:
        model = GaleriaAnimal
        fields = ['id', 'imagem']
#Serializador para ver animais e seus respectivos tutores
class AnimalUsuarioSerializer(serializers.ModelSerializer):
    tutor = "UserProfileNameSerializer(source='tutor.userprofile', read_only=True)"
    tags = serializers.SlugRelatedField(
        many = True,
        read_only = True,
        slug_field = 'nome'
    )
    class Meta:
        model = Animal
        fields = '__all__'

#Serializador para ver animais com campos nome
class AnimalSerializer(serializers.ModelSerializer):
    tutor = "UserProfileNameSerializer(source='tutor.userprofile', read_only=True)"
    raca = RacaSerializer()
    tags = TagSerializer(many = True)
    tipo_de_pelo = TipoPeloSerializer()
    cor_padrao_pelagem = CorPelagemSerializer()
    fotos = serializers.SerializerMethodField()
    class Meta:
        model = Animal
        fields = '__all__'

    def get_fotos(self, obj):
        imagens = GaleriaAnimal.objects.filter(animalgaleria__animal=obj)
        return GaleriaAnimalSpecSerializer(imagens, many=True, context = self.context).data

class AnimalSpecSerializer(serializers.ModelSerializer):
    tutor = "UserProfileNameSerializer(source='tutor.userprofile', read_only=True)"
    raca = serializers.SlugRelatedField(
        many = False,
        read_only = True,
        slug_field = 'nome'
    )
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        many = True,
        slug_field = 'nome'
    )
    tipo_de_pelo = serializers.SlugRelatedField(
        many = False,
        read_only = True,
        slug_field = 'nome'
    )
    cor_padrao_pelagem = serializers.SlugRelatedField(
        many = False,
        read_only = True,
        slug_field = 'nome'
    )
    class Meta:
        model = Animal
        fields = ['id', 'tutor', 'especie', 'nome', 'raca', 'tags', 'tipo_de_pelo', 'cor_padrao_pelagem']

class AnimalGaleriaSerializer(serializers.ModelSerializer):
    galeria = GaleriaAnimalSerializer()
    animal = AnimalSpecSerializer()
    class Meta:
        model = AnimalGaleria
        fields = "__all__"

#SERIALIZERS DE USUSARIOS

class UserSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ['id', 'username']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta():
        model = UserProfile
        fields = "__all__"

class UserProfileSpecSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        many = False,
        read_only = True,
        slug_field = 'username'
    )
    class Meta():
        model = UserProfile
        fields = ["tipo","user", "primeiro_nome_ou_nome_abrigo", "sobrenome", "email", "telefone_celular"]

class UserProfileNameSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta():
        model = UserProfile
        fields = ['user', "primeiro_nome_ou_nome_abrigo"]
        
class UserProfilePageSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(source='userprofile', read_only=True)
    animais = AnimalSerializer(many=True, source='animal_set', read_only=True)
    
    class Meta:
        model = User 
        exclude = ["password", "last_login", "is_superuser", "username", "first_name",
                "last_name", "email", "is_staff", "is_active", "date_joined", "groups", "user_permissions"]