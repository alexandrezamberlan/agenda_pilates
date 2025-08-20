# Instalar e Configurar Servidor Local para Testes de Desenvolvimento

1) Instalar o Python e Configura-lo no path do sistema operacional. 
    - Em geral ele vem instalado. Caso precise verificar, abra um terminal e no prompt digite:

        ```
            python --version
        ```

2) Instalar e configurar o git
    - Acesse e baixe o git (gerenciador de versões) utilizado. 
    - No navegador acesse e baixe o programa git - https://git-scm.com/downloads
    - Execute o instalador e configure o git no sistema operacional

3) Se for a primeira vez do repositório ou projeto na máquina local, Clonar o repositório
    - No terminal aberto, digite no prompt:

        ```
            git clone https://github.com/alexandrezamberlan/sistemaAgendamento.git
        ```

4) Se não for a primeira vez, atualize o repositório digitando em algum terminal aberto (pode ser até do VS Code):
    - No terminal aberto, digite no prompt:
        ```
            git pull
        ```

5) Se for a primeira vez do repositório ou projeto na máquina local, Criar venv (ambiente virtual ou docker para o sistema)
    - No terminal aberto, dentro da pasta do repositório clonado, digite no prompt:

        ```
            python -m venv venv
        ```

6) Ativar o ambiente virtual venv criado
    - No terminal aberto, dentro da pasta do repositório clonado, digite no prompt (para SO Windows):

        ```
            venv\Scripts\activate
        ```

7) Se for a primeira vez do repositório ou projeto na máquina local, Instalar os requirements do sistema na venv (ambiente virtual ou docker para o sistema)

    - No terminal aberto, dentro da pasta do repositório clonado, digite no prompt (para SO Windows):

        ```
            python -m pip install --upgrade pip
            python -m install -r requirements.txt
        ```
8) Se for a primeira vez do repositório ou projeto na máquina local, Criar o .env (gerenciador do ambiente virtual)
    - Crie o arquivo .env no diretório/pasta raiz do projeto clonado e coloque o conteúdo abaixo. Obs.: o arquivo deve se chamar .env

        ```
            SECRET_KEY='=%6aqk0p^aux0qvolqn_7efyj(@wh*wtc_!n10u8_o4!l#k6)h'
            DEBUG=True 
            STATIC_URL=/static/

            DOMINIO_URL='http://localhost:8000'

            EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
            EMAIL_HOST = 'smtp.gmail.com'
            EMAIL_HOST_USER = ''
            EMAIL_HOST_PASSWORD = ''
            EMAIL_PORT = 587

            EMAIL_USE_TLS = True
            EMAIL_USE_SSL = False
            EMAIL_USE_STARTTLS = False
        ```

9) Rodar ou levantar o servidor local
    - No terminal aberto, dentro da pasta do repositório clonado, digite no prompt (para SO Windows):

        ```
            python projeto\manage.py runserver
        ```

10) Acessar o sistema
    - No seu navegador de preferência, digite na barra de endereços:

        ```
            http://localhost:80000
        ```
