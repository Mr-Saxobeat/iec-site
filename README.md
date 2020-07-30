# Plataforma Web do Instituto de Estudos Climáticos da Universidade Federal do Espírito Santo (PWIEC-Ufes)

A PWIEC-Ufes visa disponiblizar ao público geral uma ferramenta para observação, consulta, estudo e compreensão dos efeitos das mudanças climáticas na região do estado do Espírito Santo.

Você pode acessar a plataforma clicando [aqui](https://mr-saxobeat.github.io/pwiec/).

![Print da plataforma](print-pwiec.png)

## Instalação (este tutorial de instalação está antigo, precisa de revisão):

Esta plataforma está sendo desenvolvida usando **python 3.8** e **pipenv 2018.11.26**.

- Instale o GDAL:
  - `sudo add-apt-repository ppa:ubuntugis/ppa`
  - `sudo apt-get update`
  - `sudo apt-get install gdal-bin`
  - `ogrinfo --version`
- Instale o *pipenv* para o gerenciamento da **virtualenv** e dos pacotes.
  - `pip install pipenv`
- Uma vez o pipenv instalado, instale a virtualenv e seus pacotes na pasta do repositório:
  - `pipenv install`
- E então ative a virtualenv:
  - `pipenv shell`
- Rode o servidor:
  - `python manage.py runserver`
- Você deve criar um arquivo `.env` que será usado pelo **python-decouple** com as seguintes variavéis:
  ````
  SECRET_KEY = "[insira sua chave gerada na instalação do django, localizado no settings.py]"
  DEBUG = "True"
  ALLOWED_HOSTS = "127.0.0.1, .localhost"
  DATABASE_URL = "[configurações do banco de dados, ver na documentação do django, ou usar o formato 'tipoDoBancoDeDados://usuario:senha@host/bancoDeDados']"
  ````
- Enfim, acesse o localhost:
  - **http://127.0.0.1:8000/**
