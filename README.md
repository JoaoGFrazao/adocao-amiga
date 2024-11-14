<h2>Apresentação</h2>

<p> Adoção Amiga é uma plataforma para unir pessoas interessadas em adotar um pet, seja ele um gato ou cachorro, com abrigos de animais. É muito comum abrigos terem dificuldades para conseguirem pessoas para adotar alguns animais, de acordo com uma pesquisa de 2020 a taxa de adoção de gatos pretos é de apenas 10%, enquanto em uma matéria do portal Metrópoles afirma que os cães pretos também são menos adotados se comparados com seus irmãos de outras cores.</p>  

<p>Do lado dos adotantes, é comum que pessoas procurem nas redes sociais seus futuros amigos procurando em várias páginas de diversos abrigos diferentes. Dessa forma o Adoção Amiga tem como objetivo ser uma plataforma para os abrigos postarem seus animais para adoção e serem encontrados pelos adotantes.</p>



<h3>1. Modelos Principais</h3>

<p> Abaixo apresento os modelos criados e seus principais campos</p>

<h4>UserProfile</h4>
<p>O modelo <code>UserProfile</code> representa o perfil do usuário, que pode ser um <em>Abrigo</em> ou um <em>Adotante</em>, associado ao modelo padrão <code>User</code> do Django.</p>

- **Campos Importantes**:
  - <code>user</code>: FK para o modelo <code>User</code>.
  - <code>tipo</code>: Indica se é um abrigo ou adotante.
  - <code>cpf</code> e <code>cnpj</code>: Obrigatórios dependendo do tipo de usuário.
  - <code>foto_logo</code>: Logo ou foto do usuário.

<h4>Animal</h4>
<p>O modelo <code>Animal</code> representa cada animal disponível para adoção ou já adotado, com detalhes de sua espécie, raça e características específicas.</p>

- **Campos Importantes**:
  - <code>tutor</code>: FK para o <code>User</code>, representa o tutor (abrigo ou adotante).
  - <code>especie</code>: Indica se o animal é um cachorro ou gato.
  - <code>raca</code>: FK para o modelo <code>Raca</code>.
  - <code>tipo_de_pelo</code>, <code>cor_padrao_pelagem</code>: FK para detalhes específicos do animal.
  - <code>foi_adotado</code>: Flag que indica se o animal já foi adotado.

<h4>Raca</h4>
<p>O modelo <code>Raca</code> define as raças disponíveis, associando-as com a espécie correspondente.</p>

- **Campos Importantes**:
  - <code>nome</code>: Nome da raça.
  - <code>especie</code>: Especifica a espécie da raça.

<h3>2. Tabelas Relacionais e Auxiliares</h3>

<h4>RacaTipo</h4>
<p>Relaciona as raças com seus tipos de pelo permitidos.</p>

- **Campos Importantes**:
  - <code>raca</code>: FK para <code>Raca</code>.
  - <code>tipo</code>: FK para <code>TipoPelo</code>.

<h4>RacaCor</h4>
<p>Relaciona as raças com suas cores permitidas de pelagem.</p>

- **Campos Importantes**:
  - <code>raca</code>: FK para <code>Raca</code>.
  - <code>cor</code>: FK para <code>CorPelagem</code>.

<h4>TipoPelo</h4>
<p>Define os tipos de pelo que um animal pode ter.</p>

- **Campos Importantes**:
  - <code>nome</code>: Nome do tipo de pelo.
  - <code>padrao</code>: Imagem ilustrativa do tipo de pelo.

<h4>CorPelagem</h4>
<p>Define as cores de pelagem possíveis para os animais.</p>

- **Campos Importantes**:
  - <code>nome</code>: Nome da cor da pelagem.
  - <code>imagem</code>: Imagem ilustrativa da cor.

<h4>Tag e AnimalTag</h4>
<p>Permitem associar palavras-chave (<code>Tag</code>) aos animais para facilitar a busca e categorização.</p>

- **Campos Importantes**:
  - <code>animal</code>: FK para <code>Animal</code>.
  - <code>tag</code>: FK para <code>Tag</code>.

<h3>3. Restrições e Regras de Validação</h3>

O sistema possui diversas restrições para garantir que os dados estejam consistentes:
- **UserProfile**: Validações específicas para abrigos e adotantes, como a obrigatoriedade de CNPJ e telefone para abrigos.
- **Animal**: Validações para garantir que cães e gatos tenham características adequadas, como a inexistência de FIV e FeLV para cães.

<h2>Quickstart</h2>

<p>Para iniciar o projeto localmente é preciso ter o Python3 instalado em seu computador, a versão utilizada foi <code>Python 3.12.2</code>. Além disso siga os passos abaixo. </p>

<ul>
    <li>Baixe ou clone esse repositório para seu computador e navegue até ele no terminal</li>
    <li>Execute o comando a seguir: <code> python venv_script.py</code></li>
    <li> Ative o ambiente virtual com <code> venv/Scripts/Activate</code> no Windows ou <code>source venv/bin/activate</code> no Linux ou Mac</li>
    <li>Em seguida faça as migrações para criar o banco de dados executando <code>python manage.py makemigrations</code></li> e posteriormente <code>python manage.py migrate</code>
    <li><strong>Opcional</strong>: para criar dados fictícios e super-usuário (username e senha: 'admin') execute o comando <code>python run_scripts.py</code></li>

Se escolheu executar o passo opcional, será criado um super-usuário que poderá ser usado para acessar o console do admin em <code>http://localhost:8000/admin</code>. Além disso todas as tabelas serão preenchidas com dados aleatórios que facilitam a navegação pelos recursos da API, as informações de login dos usuários criados com os scripts estarão escritas no arquivo de texto <code>usuarios_teste.txt</code>. As imagens foram retiradas de um dataset do Kaggle que pode ser acessado em <a>https://www.kaggle.com/datasets/chetankv/dogs-cats-images/</a>

<h2>Configuração de Throttling</h2>

<p>Para gerenciar a taxa de requisições na API, são utilizadas classes de throttling baseadas nas classes <code>AnonRateThrottle</code> e <code>UserRateThrottle</code> do Django Rest Framework. Essas classes limitam a quantidade de requisições que usuários anônimos e autenticados podem fazer em diferentes endpoints da aplicação.</p>

<h3>Classes de Throttle</h3>

<ul>
  <li>
    <h4><code>ListAnonRateThrottle</code></h4>
    <p>Esta classe estende <code>AnonRateThrottle</code> e limita o número de requisições diárias para usuários anônimos na listagem de recursos. Configuração:</p>
    <ul>
      <li>Taxa permitida: <strong>100 requisições por dia</strong></li>
    </ul>
  </li>

  <li>
    <h4><code>ListUserRateThrottle</code></h4>
    <p>Esta classe estende <code>UserRateThrottle</code> e limita o número de requisições diárias para usuários autenticados na listagem de recursos. Configuração:</p>
    <ul>
      <li>Taxa permitida: <strong>200 requisições por dia</strong></li>
    </ul>
  </li>

  <li>
    <h4><code>DetailAnonRateThrottle</code></h4>
    <p>Esta classe estende <code>AnonRateThrottle</code> e limita o número de requisições diárias para usuários anônimos em detalhes de recursos específicos. Configuração:</p>
    <ul>
      <li>Taxa permitida: <strong>150 requisições por dia</strong></li>
    </ul>
  </li>

  <li>
    <h4><code>DetailUserRateThrottle</code></h4>
    <p>Esta classe estende <code>UserRateThrottle</code> e limita o número de requisições diárias para usuários autenticados em detalhes de recursos específicos. Configuração:</p>
    <ul>
      <li>Taxa permitida: <strong>300 requisições por dia</strong></li>
    </ul>
  </li>

  <li>
    <h4><code>FilterAnonRateThrottle</code></h4>
    <p>Esta classe estende <code>AnonRateThrottle</code> e limita o número de requisições diárias para usuários anônimos ao aplicar filtros em recursos. Configuração:</p>
    <ul>
      <li>Taxa permitida: <strong>150 requisições por dia</strong></li>
    </ul>
  </li>

  <li>
    <h4><code>FilterUserRateThrottle</code></h4>
    <p>Esta classe estende <code>UserRateThrottle</code> e limita o número de requisições diárias para usuários autenticados ao aplicar filtros em recursos. Configuração:</p>
    <ul>
      <li>Taxa permitida: <strong>300 requisições por dia</strong></li>
    </ul>
  </li>
</ul>

<h3>Resumo</h3>
<p>Essas configurações de throttling ajudam a gerenciar a carga na API, prevenindo abuso e garantindo uma experiência mais estável para todos os usuários.</p>

<h2>Rotas e ViewSets</h2>

<h2>AnimalViewSet</h2>
<p>Rota para visualizar e criar registros de animais no sistema.</p>
<ul>
    <li><strong>Endpoint:</strong> /api/animals/</li>
    <li><strong>Métodos:</strong> GET, POST</li>
    <li><strong>Filtros:</strong> Busca por nome ou ID, ordenação por nome.</li>
    <li><strong>Throttle:</strong> UserRateThrottle, AnonRateThrottle</li>
</ul>

<h2>RacaViewSet</h2>
<p>Rota para visualizar e criar raças de animais.</p>
<ul>
    <li><strong>Endpoint:</strong> /api/racas/</li>
    <li><strong>Métodos:</strong> GET, POST</li>
    <li><strong>Filtros:</strong> Busca por nome ou ID, ordenação por nome.</li>
    <li><strong>Throttle:</strong> UserRateThrottle, AnonRateThrottle</li>
</ul>

<h2>TagViewSet</h2>
<p>Rota para visualizar e criar tags associadas aos animais.</p>
<ul>
    <li><strong>Endpoint:</strong> /api/tags/</li>
    <li><strong>Métodos:</strong> GET, POST</li>
    <li><strong>Filtros:</strong> Busca por nome ou ID, ordenação por nome.</li>
    <li><strong>Throttle:</strong> UserRateThrottle, AnonRateThrottle</li>
</ul>

<h2>CorPelagemViewSet</h2>
<p>Rota para visualizar e criar registros de cores de pelagem de animais.</p>
<ul>
    <li><strong>Endpoint:</strong> /api/cores-pelagem/</li>
    <li><strong>Métodos:</strong> GET, POST</li>
    <li><strong>Filtros:</strong> Busca por nome ou ID, ordenação por nome.</li>
    <li><strong>Throttle:</strong> UserRateThrottle, AnonRateThrottle</li>
</ul>

<h2>TipoPeloViewSet</h2>
<p>Rota para visualizar e criar tipos de pelo associados a raças de animais.</p>
<ul>
    <li><strong>Endpoint:</strong> /api/tipos-pelo/</li>
    <li><strong>Métodos:</strong> GET, POST</li>
    <li><strong>Filtros:</strong> Busca por ID, tipo de pelo, raça.</li>
    <li><strong>Throttle:</strong> UserRateThrottle, AnonRateThrottle</li>
</ul>

<h2>GaleriaAnimalViewSet</h2>
<p>Rota para visualizar e criar galerias de imagens para animais.</p>
<ul>
    <li><strong>Endpoint:</strong> /api/galerias-animais/</li>
    <li><strong>Métodos:</strong> GET, POST</li>
    <li><strong>Filtros:</strong> Busca por ID, espécie.</li>
    <li><strong>Throttle:</strong> UserRateThrottle, AnonRateThrottle</li>
</ul>

<h2>AnimalGaleriaViewSet</h2>
<p>Rota para associar imagens de uma galeria a um animal específico.</p>
<ul>
    <li><strong>Endpoint:</strong> /api/animais-galerias/</li>
    <li><strong>Métodos:</strong> GET, POST</li>
    <li><strong>Filtros:</strong> Busca por ID, animal, galeria, indicador de imagem principal.</li>
    <li><strong>Throttle:</strong> UserRateThrottle, AnonRateThrottle</li>
</ul>

<h2>UmGaleriaAnimal</h2>
<p>Rota para visualizar, atualizar ou deletar um registro específico de uma galeria de animal.</p>
<ul>
    <li><strong>Endpoint:</strong> /api/galeria-animal/&lt;pk&gt;/</li>
    <li><strong>Métodos:</strong> GET, PUT, DELETE</li>
    <li><strong>Throttle:</strong> DetailUserRateThrottle, DetailAnonRateThrottle</li>
</ul>

<h2>UmAnimalViewSet</h2>
<p>Rota para visualizar, atualizar ou deletar um registro específico de animal.</p>
<ul>
    <li><strong>Endpoint:</strong> /api/animal/&lt;pk&gt;/</li>
    <li><strong>Métodos:</strong> GET, PUT, DELETE</li>
    <li><strong>Filtros:</strong> Busca por nome ou ID, ordenação por nome.</li>
    <li><strong>Throttle:</strong> DetailUserRateThrottle, DetailAnonRateThrottle</li>
</ul>

<h2>AnimalGaleriaFiltro</h2>
<p>Rota para visualizar e filtrar imagens de uma galeria associadas a animais específicos.</p>
<ul>
    <li><strong>Endpoint:</strong> /api/animais-galerias-filtro/</li>
    <li><strong>Métodos:</strong> GET, PUT, DELETE</li>
    <li><strong>Filtros:</strong> Busca por ID, animal, galeria, indicador de imagem principal.</li>
    <li><strong>Throttle:</strong> FilterUserRateThrottle, FilterAnonRateThrottle</li>
</ul>

<h2>UsuarioAnimais</h2>
<p>Rota para listar todos os animais de um usuário específico.</p>
<ul>
    <li><strong>Endpoint:</strong> /api/usuario/&lt;user_pk&gt;/animais/</li>
    <li><strong>Métodos:</strong> GET</li>
    <li><strong>Throttle:</strong> FilterUserRateThrottle, FilterAnonRateThrottle</li>
</ul>

<h2>AnimaisFilter</h2>
<p>Rota para listar e filtrar animais de acordo com atributos como espécie, raça, energia e idade.</p>
<ul>
    <li><strong>Endpoint:</strong> /api/animais-filtro/</li>
    <li><strong>Métodos:</strong> GET</li>
    <li><strong>Filtros:</strong> "Espécie", "raça", "tipo_pelo", "cor_pelo", "sem_nome", "energia_max", "energia_min", "castrado", "fiv", "felv", "sociavel", "idade_min","idade_max" e "para_adocao"</li>
    <li><strong>Throttle:</strong> FilterUserRateThrottle, FilterAnonRateThrottle</li>
</ul>

<h2>Testes Realizados</h2>
<p>Para garantir a integridade do sistema, foram desenvolvidos e executados testes específicos para os modelos e serializadores do aplicativo de adoção. Abaixo, apresentamos alguns dos testes realizados:</p>

<p>Execute-os com <code> python manage.py runserver </code> </p>

<h3>1. Testes de Modelos</h3>
<h4>TestBase</h4>
<p>Uma classe base para inicializar objetos de teste e seus relacionamentos. Essa classe cria usuários com perfis de abrigo e adotante, além de animais e galeria de imagens.</p>

<h4>TestModelsAnimal</h4>
<ul>
    <li><strong>test_raca:</strong> Verifica a raça e a espécie do animal.</li>
    <li><strong>test_animal:</strong> Verifica a representação em string do animal.</li>
    <li><strong>test_animal_clean:</strong> Checa a validade dos campos <em>fiv</em> e <em>felv</em> no modelo de Animal.</li>
    <li><strong>test_animal_invalid_fiv_felv:</strong> Testa se ocorre erro de validação ao deixar os campos <em>fiv</em> e <em>felv</em> nulos.</li>
    <li><strong>test_dog_fiv_felv:</strong> Valida as restrições de <em>fiv</em> e <em>felv</em> para cães.</li>
    <li><strong>test_animal_invalid_raca_especie:</strong> Valida a compatibilidade entre a raça e a espécie do animal.</li>
    <li><strong>test_animal_sem_raca:</strong> Confirma que a ausência de raça não gera erro.</li>
    <li><strong>test_animal_invalid_adoption_status:</strong> Verifica se o estado de adoção está configurado corretamente.</li>
    <li><strong>test_animal_invalid_profile:</strong> Garante que apenas abrigos possam colocar animais para adoção.</li>
    <li><strong>test_energia_range_min e test_energia_range_max:</strong> Testam o limite dos valores para o campo de energia do animal.</li>
</ul>

<h4>TestModelsUser</h4>
<ul>
    <li><strong>test_abrigo_attrs:</strong> Valida campos obrigatórios no perfil do abrigo, como telefone e UF.</li>
    <li><strong>test_abrigo_attrs_clean:</strong> Garante que CPF e sobrenome sejam nulos em perfis de abrigo.</li>
</ul>

<h4>TestModelsCaracteristicas</h4>
<ul>
    <li><strong>test_galeria_animal:</strong> Verifica se o campo <em>especie</em> está correto na galeria de imagens.</li>
    <li><strong>test_tag:</strong> Valida as tags associadas ao animal.</li>
    <li><strong>test_tipo_pelo:</strong> Verifica a associação do tipo de pelo.</li>
    <li><strong>test_cor_pelagem:</strong> Valida a cor da pelagem do animal.</li>
</ul>

<h3>2. Testes de Serializadores</h3>
<p>Esses testes garantem que os dados serializados possuam os campos esperados e estejam estruturados corretamente.</p>
<ul>
    <li><strong>teste_verifica_campos_serializados_de_raca:</strong> Valida os campos da <em>RacaSerializer</em>.</li>
    <li><strong>teste_verifica_campos_serializados_de_tag:</strong> Verifica os campos da <em>TagSerializer</em>.</li>
    <li><strong>teste_verifica_campos_serializados_de_tipo_pelo:</strong> Confirma a estrutura da <em>TipoPeloSerializer</em>.</li>
    <li><strong>teste_verifica_campos_serializados_de_cor_pelagem:</strong> Valida os campos de <em>CorPelagemSerializer</em>.</li>
    <li><strong>teste_verifica_campos_serializados_de_galeria_animal:</strong> Garante os campos de <em>GaleriaAnimalSerializer</em>.</li>
    <li><strong>teste_verifica_campos_serializados_de_animal_usuario:</strong> Valida os campos de <em>AnimalUsuarioSerializer</em> e <em>AnimalSerializer</em>.</li>
</ul>



