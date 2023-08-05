# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynalytics',
 'pynalytics.data_pipeline',
 'pynalytics.data_pipeline.feature_engineering',
 'pynalytics.data_pipeline.pre_processing',
 'pynalytics.parser']

package_data = \
{'': ['*'], 'pynalytics': ['yamls/*']}

install_requires = \
['Jinja2==3.1.2',
 'MarkupSafe==2.1.1',
 'Pillow==9.4.0',
 'PyYAML==6.0',
 'altair==4.2.0',
 'attrs==22.2.0',
 'bpemb==0.3.4',
 'certifi==2022.12.7',
 'charset-normalizer==2.1.1',
 'contourpy==1.0.6',
 'coverage==7.0.2',
 'cycler==0.11.0',
 'entrypoints==0.4',
 'exceptiongroup==1.1.0',
 'fonttools==4.38.0',
 'gensim==3.8.3',
 'idna==3.4',
 'importlib-resources==5.10.2',
 'iniconfig==1.1.1',
 'joblib==1.2.0',
 'jsonschema==4.17.3',
 'kiwisolver==1.4.4',
 'matplotlib==3.6.2',
 'numpy==1.24.1',
 'packaging==22.0',
 'pandas==1.5.2',
 'pkgutil-resolve-name==1.3.10',
 'pluggy==1.0.0',
 'pyparsing==3.0.9',
 'pyrsistent==0.19.3',
 'pytest-cov==4.0.0',
 'pytest==7.2.0',
 'python-dateutil==2.8.2',
 'pytz==2022.7',
 'requests==2.28.1',
 'scikit-learn==1.2.0',
 'scipy==1.9.3',
 'sentencepiece==0.1.97',
 'six==1.16.0',
 'smart-open==6.3.0',
 'threadpoolctl==3.1.0',
 'tomli==2.0.1',
 'toolz==0.12.0',
 'tqdm==4.64.1',
 'urllib3==1.26.13',
 'whatlies==0.7.0',
 'zipp==3.11.0']

entry_points = \
{'console_scripts': ['main = pynalytics.main:']}

setup_kwargs = {
    'name': 'pynalytics',
    'version': '0.1.0',
    'description': 'This is a lib from developed for the individual work related to the Software Evolution and Configuration Management subject from UnB - Universidade de Brasília during the 2022.2 semester',
    'long_description': '# Trabalho individual de GCES 2022-2\n\n\nOs conhecimentos de Gestão de Configuração de Software são fundamentais no ciclo de vida de um produto de software. As técnicas para a gestão vão desde o controle de versão, automação de build e de configuração de ambiente, testes automatizados, isolamento do ambiente até o deploy do sistema. Todo este ciclo nos dias de hoje são integrados em um pipeline de DevOps com as etapas de Integração Contínua (CI) e Deploy Contínuo (CD) implementadas e automatizada.\n\nPara exercitar estes conhecimentos, neste trabalho, você deverá aplicar os conceitos estudados ao longo da disciplina no produto de software contido neste repositório.\n\nO sistema se trata de uma biblioteca python para executar pipelines de dados de forma customizável em bancos de dados.\n\nPara executar a aplicação em sua máquina, basta seguir o passo-a-passo descritos abaixo.\n\n# Resumo da aplicação \n\n A biblioteca desenvolvida auxilia desenvolvedores a explorar os dados com funções essenciais para a identificação de outliers e anomalias e uma interface que auxilia a visualizar as informações de acordo com o arquivo de configuração.\n\n A biblioteca recebe um arquivo yaml com as configurações de cada etapa do pipeline de dados, e do endereço do banco de dados.\n Após a execução do banco de dados, o banco de dados de dados é atualizado com os resultados da análise e os resultados podem ser visualizados por meio de dashboards no metabase.\n\n # Etapas do Trabalho\n\n O trabalho deve ser elaborado através de etapas. Cada uma das etapas deve ser realizada em um commit separado com o resultado funcional desta etapa.\n\nAs etapas de 1 a 3 são relacionadas ao isolamento do ambiente utilizando a ferramenta Docker e Docker Compose. Neste sentido o tutorial abaixo cobre os conceitos fundamentais para o uso destas tecnologias.\n\n[Tutorial de Docker](https://github.com/FGA-GCES/Workshop-Docker-Entrega-01/tree/main/tutorial_docker)\n\nAs etapas de 4 e 5 são relacionadas à configuração do pipeline de CI e CD.\n\n[Tutorial CI - Gitlab](https://github.com/FGA-GCES/Workshop-CI-Entrega-02/tree/main/gitlab-ci_tutorial)\n\n\n## Containerização do Banco\n\n\nA versão inicial do sistema contém o metabase no backend cujo funcionamento requer uma instalação de um banco de dados Mongo. A primeira etapa do trabalho é de configurar um container somente para o banco de dados com as credenciais especificadas na descrição da aplicação e testar o funcionamento do mesmo.\n\n## Containerização da aplicação + metabase\n\nNesta etapa, tanto o a aplicação python quanto o metabase/banco deverão estar funcionando em containers individuais.\n\nDeverá ser utilizado um orquestrador (Docker Compose) para gerenciar comunicação entre os containers além do uso de credenciais, networks, volumes, entre outras configurações necessárias para a correta execução da aplicação.\n\n## Gestão de dependencias e pacotes python\n\nConfigurar o gerenciador de dependencias e pacotes python, o poetry, para gerar um pacote pip da solução. Publicar a biblioteca\n\nhttps://python-poetry.org\n\n## Documentação automatizada\n\nGerar a documentação da biblioteca de forma automatizada utilizando o doxygen para gerar informacoes da biblioteca e o sphinx para criar documentação https://www.sphinx-doc.org\n\n\n\n##  Integração Contínua (CI)\n\nPara a realização desta etapa, a aplicação já deverá ter seu ambiente completamente containerizado.\n\nDeverá ser utilizada uma ferramenta de Integração Contínua para garantir o build, os testes e o deploy para o https://pypi.org .\n\nEsta etapa do trabalho poderá ser realizada utilizado os ambientes de CI do GitLab-CI ou Github Actions.\n\nRequisitos da configuração da Integração Contínua (Gitlab ou Github) incluem:\n\nBuild (Poetry)\nTest - unitários\nLint - \nDocumentação (sphinx)\n\n\n## Avaliação\n\nA avaliação do trabalho será feita à partir da correta implementação de cada etapa. A avaliação será feita de maneira **quantitativa** (se foi realizado a implementação + documentação), e **qualitativa** (como foi implementado, entendimento dos conceitos na prática, complexidade da solução). Para isso, faça os **commits atômicos, bem documentados, completos** a fim de facilitar o entendimento e avaliação do seu trabalho. Lembrando o trabalho é individual.\n\n**Observações**: \n1. A data final de entrega do trabalho é o dia 28/01/2023;\n2. O trabalho deve ser desenvolvido em um **repositório PESSOAL e PRIVADO** que deverá ser tornado público somente após a data de entrega do trabalho (no dia 28/01/2023);\n3. Cada etapa do trabalho deverá ser entregue em commits progressivos (pendendo ser mais de um commit por etapa);\n4. Os **commits devem estar espaçados em dias ao longo do desenvolvimento do trabalho**. Commits feitos todos juntos na data de entrega não serão descontados da nota final.\n\n| Item | Peso |\n|---|---|\n| 1. Containerização do Banco                      | 1.0 |\n| 2. Containerização da biblioteca + Banco          | 1.5 |\n| 3. Publicação da biblioteca  | 1.5 |\n| 4. Documentação automatiza | 1.5 |\n| 5. Integração Contínua (Build, Test, Lint, documentacao)       | 3.0 |\n| 6. Deploy Contínuo                               | 1.5 |\n\n\n##  Exemplo de Trabalhos Anteriores\n\nAlguns trabalhos de trabalhos anteriores:\n\n- [2020/2](https://github.com/FGA-GCES/Trabalho-Individual-2020-2)\n- [2021/1](https://github.com/FGA-GCES/Workshop-Docker-Entrega-01)\n- [2021/2](https://github.com/FGA-GCES/Trabalho-Individual-2021-2)\n\n\n\n### Requisitos de instação\n\n```\npython -m venv env\nsource env/bin/activate\npip install -r requirements.txt\n```\n\n### Rodando a aplicação\n\n```\npython src/main.py\n```\n\n### Testando\n\n```\npytest --cov\n```\n\n### Metabase\n\nO metabase ajuda a visualizar e a modelar o processamento dos dados, a engenharia de features e monitoramento do modelo.\n\n\n\n| Keywords  | Descrição |\n|-----------|-------------|\n|   CSV     | Um arquivo CSV é um arquivo de texto simples que armazena informações de tabelas e planilhas. Os arquivos CSV podem ser facilmente importados e exportados usando programas que armazenam dados em tabelas.|\n| Collection (coleção)| Uma coleção é um agrupamento de documentos do MongoDB. Os documentos dentro de uma coleção podem ter campos diferentes. Uma coleção é o equivalente a uma tabela em um sistema de banco de dados relacional.|\n|  Database | Um banco de dados armazena uma ou mais coleções de documentos.|\n| Mongo| É um banco de dados NoSQL desenvolvido pela MongoDB Inc. O banco de dados MongoDB foi criado para armazenar uma grande quantidade de dados e também executar rapidamente.|\n\n\n\n**Connect the database to the metabase**\n\n- step 1: Open localhost:3000\n- step 2: Click Admin setting\n- step 3: Click Database\n- step 4: Adicione os dados de autenticação de  banco de dados \n\n\n**Exemplo da conexão mongo  metabase**\n|  metabase  | credential  |\n|------------|-------------|\n|    host    |  mongo  |\n|dabase_name | use the name you define in make migrate|\n|    user    |   lappis    |\n|  password  |   lappis    |\n\n',
    'author': 'João Pedro Chaves',
    'author_email': 'joaopedroaschaves@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/JPedroCh/Trabalho-Individual-2022-2',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '==3.9.7',
}


setup(**setup_kwargs)
