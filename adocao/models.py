from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

#Opções para campos choice
ESPECIE_CHOICES = [
    ('cachorro', 'Cachorro'),
    ('gato', 'Gato')
]
ENERGIA_CHOICES = [1, 2, 3, 4, 5]

UF_CHOICES = [('AC', 'ac'), ('AL', 'al'), ('AP', 'ap'), ('AM', 'am'), ('BA', 'ba'), ('CE', 'ce'), ('DF', 'df'), ('ES', 'es'),  ('GO', 'go'),
    ('MA', 'ma'), ('MT', 'mt'), ('MS', 'ms'), ('MG', 'mg'), ('PA', 'pa'), ('PB', 'pb'), ('PR', 'pr'), ('PE', 'pe'), ('PI', 'pi'), ('RJ', 'rj'),
    ('RN', 'rn'), ('RS', 'rs'), ('RO', 'ro'), ('RR', 'rr'), ('SC', 'sc'),('SP', 'sp'), ('SE', 'se'), ('TO', 'to')]

#Funções para validar entrada no banco de dados
def profile_por_user(tutor):
    usuario = get_object_or_404(UserProfile, user = tutor)
    usuario = usuario.tipo
    return usuario

def  raca_especie(especie):
    racas_possiveis = Raca.objects.filter(Q(especie = especie.lower()) | Q(especie = especie.capitalize()))
    return racas_possiveis

#Tabelas
class GaleriaAnimal(models.Model):
    especie = models.CharField(choices=ESPECIE_CHOICES, max_length=10, null=True)
    imagem = models.ImageField(upload_to='fotos_animal/%Y/%m/%d', null=False, blank= False, default="usuario_sem_foto.png")
    def __int__(self):
        return id

    
class Tag(models.Model):
    nome = models.CharField(max_length=50)
    def __str__(self):
        return self.nome

class TipoPelo(models.Model):
    nome = models.CharField(max_length=50)
    imagem = models.ImageField(upload_to='fotos_tipopelo/%Y/%m/%d', null=False, blank= False, default="usuario_sem_foto.png")
    def __str__(self):
        return self.nome

class CorPelagem(models.Model):
    nome = models.CharField(max_length=50)
    imagem = models.ImageField(upload_to='fotos_cor/%Y/%m/%d', null=False, blank= False, default="usuario_sem_foto.png")
    def __str__(self):
        return self.nome

class Raca(models.Model):       
    nome = models.CharField(max_length=255)
    especie = models.CharField(max_length=10, choices=ESPECIE_CHOICES)  # Relaciona a espécie com a raça
    tipos_pelo_possiveis = models.ManyToManyField(TipoPelo)
    cores_pelo_possiveis = models.ManyToManyField(CorPelagem)
    def __str__(self):
        return self.nome

class Animal(models.Model):
    #ForeignKeys
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)
    especie = models.CharField(max_length=10, choices=ESPECIE_CHOICES)
    raca = models.ForeignKey(Raca, on_delete=models.SET_NULL, null=True, blank=False)
    tipo_de_pelo = models.ForeignKey(TipoPelo, on_delete=models.SET_NULL, null=True, blank=True) 
    cor_padrao_pelagem = models.ForeignKey(CorPelagem, on_delete=models.SET_NULL, null=True, blank=True)
   
    nome = models.CharField(max_length=255)
    descricao = models.TextField(null=True, blank=True)
    energia = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])    
    esta_para_adocao = models.BooleanField(default=False, null=False)
    foi_adotado = models.BooleanField(default=False, null=True)
    castrado = models.BooleanField(default=False)
    fiv = models.BooleanField(null=True, blank=True)
    felv = models.BooleanField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    fotos = models.ManyToManyField(GaleriaAnimal, through='AnimalGaleria')

    sociavel_com_animais = models.BooleanField(null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    mostrar_no_perfil = models.BooleanField(default=True)

    def clean(self):
        # Verificação para definir restrições específicas para cães e gatos
        if self.especie in ESPECIE_CHOICES[0]:
            self.fiv = None  # Cães não têm FIV
            self.felv = None  # Cães não têm FeLV

        if self.especie in ESPECIE_CHOICES[1]:
            if self.fiv is None or self.felv is None:
                raise ValidationError("Para gatos é preciso informar se são FIV ou FeLV")

        if self.raca is None:
            if not self.tipo_de_pelo or not self.cor_padrao_pelagem:
                raise ValidationError("Para raça SRD, é necessário definir o tipo e a cor da pelagem.")
        
        #Verificações para animais de abrigos
        if profile_por_user(self.tutor.id) == 'Abrigo' or profile_por_user(self.tutor.id) == 'abrigo':
            if self.nome ==  '' or self.nome is None:
                self.nome = ('Pet Ainda Sem Nome')

            if self.descricao == '' or self.descricao is None:
                raise ValidationError("Escreva uma descrição para o pet")
            
            if self.data_nascimento is None:
                raise ValidationError("Se não souber a data de nascimento exata coloque primeiro de janeiro do ano de nascimento do pet")
            
            if self.foi_adotado == None:
                raise ValidationError("Para animais de abrigo é preciso informar se foi adotado")
            
        if self.raca != None:
            if self.especie not in raca_especie(self.especie):
                raise ValidationError(f'Essa raça não é de {self.especie}')
            
            if self.tipo_de_pelo not in self.raca.tipos_pelo_possiveis.all():
                raise ValidationError(f'Esse tipo de pelo não é válido para raça {self.raca}')
            
            if self.cor_padrao_pelagem not in self.raca.cores_pelo_possiveis.all():
                raise ValidationError(f'Esse tipo de pelo não é válido para raça {self.raca}')
        
        if self.esta_para_adocao == True and self.foi_adotado == True:
            raise ValidationError('O animal não pode estar para adoção e ter sido adotado ao mesmo tempo')
        
        if profile_por_user(self.tutor.id) == 'Adotante' or profile_por_user(self.tutor.id) == 'adotante':
                if self.esta_para_adocao == True:
                    raise ValidationError('Somente animais de abrigo podem estar para adoção')
        
    def __str__(self):
        return self.nome

class AnimalGaleria(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    galeria = models.ForeignKey(GaleriaAnimal, on_delete=models.CASCADE)
    isMain = models.BooleanField(null=False, default=False)

    def __str__(self):
        return str(self.galeria.id)

#Tabelas de usuarios

class GaleriaUser(models.Model):
    imagem = models.ImageField(upload_to='fotos/%Y/%m/%d', null=False, blank= False, default="usuario_sem_foto.png")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    isMain = models.BooleanField(null=False, default=False)

    def clean(self):
        # Verifica se a imagem está marcada como principal (isMain=True)
        if self.isMain:
            # Verifica se já existe uma imagem principal para o mesmo objeto
            existing_images = GaleriaUser.objects.filter(
                content_type=self.content_type,
                object_id=self.object_id,
                isMain=True
            )

            # Se já existir uma imagem principal, levanta um erro de validação
            if existing_images.exists():
                raise ValidationError("Este objeto já tem uma imagem principal.")

    def __str__(self):
        return f"Imagem associada a {self.content_object}"



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Campos gerais
    primeiro_nome_ou_nome_abrigo = models.CharField(max_length=255)
    sobrenome = models.CharField(max_length=255, null=True, blank=True)  # Obrigatório para adotante
    cpf = models.CharField(max_length=14, null=True, blank=True)  # Obrigatório para adotante
    cnpj = models.CharField(max_length=18, null=True, blank=True)  # Obrigatório para abrigo
    email = models.EmailField(max_length=255, null=False, blank=False)
    telefone_celular = models.CharField(max_length=15, null=True, blank=True)  # Obrigatório para abrigo
    endereco = models.CharField(max_length=255, null=True, blank=True)
    uf = models.CharField(max_length=2, choices=UF_CHOICES)
    tipo = models.CharField(max_length=10, choices=[('abrigo', 'Abrigo'), ('adotante', 'Adotante')])
    descricao = models.TextField(null=True, blank=True)  # Obrigatório para abrigo
    animais_em_casa = models.BooleanField(null=True, blank=True)
    buscando_oferecendo = models.CharField(max_length=10, choices=[('cachorro', 'Cachorro'), ('gato', 'Gato'), ('ambos', 'Ambos')], null=True, blank=True)
    foto_logo = models.ManyToManyField(GaleriaUser)
    
    def clean(self):
        from django.core.exceptions import ValidationError
        # Verificações de constraints
        if self.tipo == 'abrigo' or self.tipo == 'Abrigo':
            self.cpf = None
            self.sobrenome = None
            if not self.telefone_celular:
                raise ValidationError("Telefone/Celular é obrigatório para abrigos.")
            if not self.cnpj:
                raise ValidationError("CNPJ é obrigatório para abrigos.")
            if not self.descricao or self.descricao == '':
                raise ValidationError("Descrição é obrigatória para abrigos.") 
            if not self.uf:
                raise ValidationError("UF é obrigatório para abrigos.")
            if not self.uf:
                raise ValidationError("UF é obrigatório para abrigos.")
        else:
            self.cnpj = None
            if not self.sobrenome:
                raise ValidationError("Sobrenome é obrigatório para adotantes.")
            if not self.primeiro_nome_ou_nome_abrigo:
                raise ValidationError("Primeiro Nome é obrigatório para adotantes.")

    def __str__(self):
        return self.id