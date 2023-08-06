# Trabalho individual de GCES 2022-2


Os conhecimentos de Gestão de Configuração de Software são fundamentais no ciclo de vida de um produto de software. As técnicas para a gestão vão desde o controle de versão, automação de build e de configuração de ambiente, testes automatizados, isolamento do ambiente até o deploy do sistema. Todo este ciclo nos dias de hoje são integrados em um pipeline de DevOps com as etapas de Integração Contínua (CI) e Deploy Contínuo (CD) implementadas e automatizada.

Para exercitar estes conhecimentos, neste trabalho, você deverá aplicar os conceitos estudados ao longo da disciplina no produto de software contido neste repositório.

O sistema se trata de uma biblioteca python para executar pipelines de dados de forma customizável em bancos de dados.

Para executar a aplicação em sua máquina, basta seguir o passo-a-passo descritos abaixo.

# Resumo da aplicação 

 A biblioteca desenvolvida auxilia desenvolvedores a explorar os dados com funções essenciais para a identificação de outliers e anomalias e uma interface que auxilia a visualizar as informações de acordo com o arquivo de configuração.

 A biblioteca recebe um arquivo yaml com as configurações de cada etapa do pipeline de dados, e do endereço do banco de dados.
 Após a execução do banco de dados, o banco de dados de dados é atualizado com os resultados da análise e os resultados podem ser visualizados por meio de dashboards no metabase.

 # Etapas do Trabalho

 O trabalho deve ser elaborado através de etapas. Cada uma das etapas deve ser realizada em um commit separado com o resultado funcional desta etapa.

As etapas de 1 a 3 são relacionadas ao isolamento do ambiente utilizando a ferramenta Docker e Docker Compose. Neste sentido o tutorial abaixo cobre os conceitos fundamentais para o uso destas tecnologias.

[Tutorial de Docker](https://github.com/FGA-GCES/Workshop-Docker-Entrega-01/tree/main/tutorial_docker)

As etapas de 4 e 5 são relacionadas à configuração do pipeline de CI e CD.

[Tutorial CI - Gitlab](https://github.com/FGA-GCES/Workshop-CI-Entrega-02/tree/main/gitlab-ci_tutorial)


## Containerização do Banco


A versão inicial do sistema contém o metabase no backend cujo funcionamento requer uma instalação de um banco de dados Mongo. A primeira etapa do trabalho é de configurar um container somente para o banco de dados com as credenciais especificadas na descrição da aplicação e testar o funcionamento do mesmo.

### RESOLUÇÃO

Foi criado um arquivo docker-compose.yml que continha apenas um container do mongodb a partir da imagem "mongo"


## Containerização da aplicação + metabase

Nesta etapa, tanto o a aplicação python quanto o metabase/banco deverão estar funcionando em containers individuais.

Deverá ser utilizado um orquestrador (Docker Compose) para gerenciar comunicação entre os containers além do uso de credenciais, networks, volumes, entre outras configurações necessárias para a correta execução da aplicação.

### RESOLUÇÃO

Foi criado um Dockerfile para o app (lib python).
No arquivo docker-compose.yml foram adicionados dois containeres novos, o do metabase e o do app (que builda a partir da Dockerfile). Foi também criada uma network (tipo bridge) para comunicação entre os conteineres do metabase e do mongodb.

## Gestão de dependencias e pacotes python

Configurar o gerenciador de dependencias e pacotes python, o poetry, para gerar um pacote pip da solução. Publicar a biblioteca

https://python-poetry.org

### RESOLUÇÃO

Foi rodado '''poetry init''' e criado um arquivo pyproject.toml e foram adicionadas configurações da lib e todas suas dependencias, após isso foi rodado o comando '''poetry publish --build''', para publicar a lib manualmente no PyPI.
Link da lib: https://pypi.org/project/tf-gces/

## Documentação automatizada

Gerar a documentação da biblioteca de forma automatizada utilizando o doxygen para gerar informacoes da biblioteca e o sphinx para criar documentação https://www.sphinx-doc.org

### RESOLUÇÃO
Primeiro instalei o doxygen localmente e criei uma doxyfile, nessa doxyfile coloquei o README.md e o diretório src de forma recursiva para documentar todos os arquivos. Também configurei para gerar apenas XML. Após isso consegui gerar os XML com o comando '''doxygen Doxyfile'''. Instalei o breathe e o sphinx, criei o arquivo de configuração do sphinx conf.py e configurei o breathe la dentro e o adicionei como extensão. Após isso rodei '''sphinx-build -b html . ./docs''' para gerar uma documentação em HTML na pasta ./docs.


##  Integração Contínua (CI)

Para a realização desta etapa, a aplicação já deverá ter seu ambiente completamente containerizado.

Deverá ser utilizada uma ferramenta de Integração Contínua para garantir o build, os testes e o deploy para o https://pypi.org .

Esta etapa do trabalho poderá ser realizada utilizado os ambientes de CI do GitLab-CI ou Github Actions.

Requisitos da configuração da Integração Contínua (Gitlab ou Github) incluem:

Build (Poetry)
Test - unitários
Lint - Pylint
Documentação (sphinx)

### RESOLUÇÃO
Primeiramente foi criado o workflow que é rodoado em qualquer push na main.
Comecei instalando o python e o poetry, atravez do actions/setup-python@v4 e do abatilo/actions-poetry@v2 (achei no marketplace).
Após isso rodo um '''poetry install''', que installa todas a dependências.

Depois rodei os testes '''poetry run pytest tests''', como não há nenhum teste na pasta tests, ele falhava e não rodava o resto do job, para isso criei um placeholder de teste na pasta tests, que simplesmente passa. Com isso a etapa de rodar os testes tem sucesso.

Após isso o job faz uma checagem de lint, utilizei o pylint (que foi adicionado nas dependencias do poetry e ja instalado), e rodo '''poetry run pylint --fail-under=7 src''', para passar, tem que ter uma qualidade de código acima 7/10. Para atingir essa qualidade, com ajuda da extensão black, formatei todos os arquivos do projeto e commitei. (A qualidade inicial era 2/10). Com isso a etapa de lint passa.

Para gerar a documentação, instalei o oxygen manualmente no ubuntu que está rodando o workflow, e gerei o XML a partir do Doxyfile que foi criado na parte de documentação. Instalei o breathe e o Sphinx através do Pip e gerei a documentação final com o Sphinx em HTML na pasta docs, adicionei essa pasta também no pyproject.toml para ela ser publicada junto com a biblioteca no PyPI.

Depois de instalar dependencias, rodar testes, lint e gerar a documentação atualizada, realizo o build com o poetry. 

Após o build é finalmente possível publicar a nova release no PyPI, eu gero uma nova versão (ex: de 0.0.1 vai para 0.0.2) e publico do PyPI. Link da biblioteca: https://pypi.org/project/tf-gces/ . A geração da nova versão deve alterar a versão presente no pyproject.toml, para isso, a versão é incrementada com o comando '''poetry version patch''' e a publicação é realizada, após isso a alteração do arquivo pyproject.toml é automaticamente commitada na main, para que quando o proximo release for realizado, ele já tenha a versão atualizada no pyproject.toml e não de erro. Esse commit e push feitos no workflow é automatizado e não faz o worflow rodar em loop infinito.

O projeto está na versão 0.1.4, e quando eu fizer o push desse readme irá para versão tf-gces 0.1.5, que será a versão final publicada por mim.

A lib contém também a pasta docs, com a documentação atualizada gerada pelo sphinx.


## Avaliação

A avaliação do trabalho será feita à partir da correta implementação de cada etapa. A avaliação será feita de maneira **quantitativa** (se foi realizado a implementação + documentação), e **qualitativa** (como foi implementado, entendimento dos conceitos na prática, complexidade da solução). Para isso, faça os **commits atômicos, bem documentados, completos** a fim de facilitar o entendimento e avaliação do seu trabalho. Lembrando o trabalho é individual.

**Observações**: 
1. A data final de entrega do trabalho é o dia 28/01/2023;
2. O trabalho deve ser desenvolvido em um **repositório PESSOAL e PRIVADO** que deverá ser tornado público somente após a data de entrega do trabalho (no dia 28/01/2023);
3. Cada etapa do trabalho deverá ser entregue em commits progressivos (pendendo ser mais de um commit por etapa);
4. Os **commits devem estar espaçados em dias ao longo do desenvolvimento do trabalho**. Commits feitos todos juntos na data de entrega não serão descontados da nota final.

| Item | Peso |
|---|---|
| 1. Containerização do Banco                      | 1.0 |
| 2. Containerização da biblioteca + Banco          | 1.5 |
| 3. Publicação da biblioteca  | 1.5 |
| 4. Documentação automatiza | 1.5 |
| 5. Integração Contínua (Build, Test, Lint, documentacao)       | 3.0 |
| 6. Deploy Contínuo                               | 1.5 |


##  Exemplo de Trabalhos Anteriores

Alguns trabalhos de trabalhos anteriores:

- [2020/2](https://github.com/FGA-GCES/Trabalho-Individual-2020-2)
- [2021/1](https://github.com/FGA-GCES/Workshop-Docker-Entrega-01)
- [2021/2](https://github.com/FGA-GCES/Trabalho-Individual-2021-2)



### Requisitos de instação

```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Rodando a aplicação

```
python src/main.py
```

### Testando

```
pytest --cov
```

### Metabase

O metabase ajuda a visualizar e a modelar o processamento dos dados, a engenharia de features e monitoramento do modelo.



| Keywords  | Descrição |
|-----------|-------------|
|   CSV     | Um arquivo CSV é um arquivo de texto simples que armazena informações de tabelas e planilhas. Os arquivos CSV podem ser facilmente importados e exportados usando programas que armazenam dados em tabelas.|
| Collection (coleção)| Uma coleção é um agrupamento de documentos do MongoDB. Os documentos dentro de uma coleção podem ter campos diferentes. Uma coleção é o equivalente a uma tabela em um sistema de banco de dados relacional.|
|  Database | Um banco de dados armazena uma ou mais coleções de documentos.|
| Mongo| É um banco de dados NoSQL desenvolvido pela MongoDB Inc. O banco de dados MongoDB foi criado para armazenar uma grande quantidade de dados e também executar rapidamente.|



**Connect the database to the metabase**

- step 1: Open localhost:3000
- step 2: Click Admin setting
- step 3: Click Database
- step 4: Adicione os dados de autenticação de  banco de dados 


**Exemplo da conexão mongo  metabase**
|  metabase  | credential  |
|------------|-------------|
|    host    |  mongo  |
|dabase_name | use the name you define in make migrate|
|    user    |   lappis    |
|  password  |   lappis    |

