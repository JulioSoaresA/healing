# Healing

Este projeto é um sistema de consultas médicas online que permite que médicos e pacientes interajam de maneira eficiente e prática. O sistema possibilita o agendamento de consultas, acompanhamento de pacientes e gestão de atendimentos, integrando funcionalidades como videoconferência e criação de eventos no Google Agenda.
Funcionalidades
Funcionalidades para Médicos

## Funcionalidades para Médicos

  - [x] Cadastro de horários disponíveis
  - [x] Atendimento de Pacientes com Consulta Marcada:
  - [x] Cadastro de Documentos do Paciente:
  - [x] Cadastro de Link para Videoconferência (Google Meet):
  - [x] Finalização de Consultas:
  - [x] Criação de Evento no Google Agenda:
  - [x] Visualização de Consultas Agendadas:
  - [x] Dashboard com Filtros de Consultas:

## Funcionalidades para Pacientes

  - [x] Marcar Consulta com o Médico:
  - [x] Visualizar Consultas Agendadas:
  - [x] Entrar em uma Consulta Marcada:
  - [x] Entrar na Videoconferência (Google Meet):

## Tecnologias utilizadas

  - Python 3.10+
  - Django 5.1
  - SQLite

## Instalação
### Instalação de Ambiente Virtual
- Baixe esse repositório e entre no diretório respectivo
  ```bash
  git clone https://github.com/JulioSoaresA/healing.git
  ```
  ```bash
  cd healing
  ```
- Utilize um VirtualEnvironment<br>
  ```bash
  python -m venv venv
  ```
- Instale as dependências necessárias<br>
  ```bash
  pip install -r requirements.txt
  ```
- Realize as migrações do banco de dados
  ```bash
  python manage.py migrate
  ```
- Crie um superusuário para acessar o painel de administração
  ```bash
  python manage.py createsuperuser
  ```
- Inicie o servidor
  ```bash
  python manage.py runserver
  ```
