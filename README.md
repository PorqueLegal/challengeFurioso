# Documento do Chatbot 
## Introdução
Esse é um chatbot para o Telegram desenvolvido em Python, que tem objetivo de auxiliar os torcedores da Furia de CS a ficar mais atualizados sobre o cenário. Ele utiliza a Api do Telegram para acontecer a interação com os usuários.
 

## Funcionalidade
	- Responde a comandos específicos;
	- Ajuda nas pesquisas e para o usuário se atualizar de forma mais ágil;
	- Com mais algumas funcionalidades, o usuário teria um perfil no chatbot mostrando que é realmente um fã.

## Comandos
	### Inicia o bot:
	-/start 
	### Opções para o usuário achar as informações que deseja:
	-/menu	
	### Dados do Usuário:
	-/dados
	### Mudar o nome:
	-/mudarNome
	### Mostrar os comandos:
	-/help

## Tecnologia utilizada:
    - HTML/CSS;
    - bootstrap 5.3.5;
    - telegram;
    - python.

## Requisitos
	Para funcionar o bot, é necessário instalar em seu sistema os itens:
	- pip install python-telegram-bot ou pip install python-telegram-bot --upgrade
    - pip install beautifulsoup4
    - pip install -r requirements.txt
    - pip install requests
    - pip install selenium
    - pip install python-dotenv

## Versão:
	- Python 3.8 ou superior
	- Bootstrap 5.3.5

## Como rodar o projeto:
    Baixe o Github antes de fazer as seguintes
    1. Clone este repositório para o seu computador: 
        ```bash
            git clone https://github.com/PorqueLegal/challengeFurioso.git
         ```          

    2. Instale as dependências: 
    ``bash
        pip install -r requirements.txt
    ```
    
    3. Crie um arquivo `.env` para armazenar o token do seu bot:
    - Na raiz do projeto, crie um arquivo chamado `.env` e adicione o seguinte conteúdo:
        ```
        TELEGRAM_BOT_TOKEN=seu_token_aqui
        ```

    4. Certifique-se de que o arquivo `.env` está listado no `.gitignore` para evitar que ele seja enviado ao GitHub.

## Como rodar os testes:
    1. Execute o bot: 
    
        ```bash
            telegram_chatbot.py
        ```

    2. No Telegram, inicie uma conversa com o seu bot e envie comandos para testar.


## Estrutura do Projeto
    ```
    index.html ###arquivo para pagina web
    
    style.css ###estilização da pagina web

    README.md #Este arquivo

    chatbot/
    |
    ├── .env ###Arquivo com o token
    ├── .gitignore ###Lista de arquivos e pastas ignoradas pelo Git
    ├── requirements.txt ###Lista de depêndencias do projeto
    └── telegram_chatbot.py ###Codigo para rodar o bot
    ```


## Próximos passos:
    - Colocar mais informações dos jogadores, como KD e replays;
    - Colocar notificação para informar o usuário das novidades.
    - Colocar mais variavel para complementar as informações do usuário, como desde quanto ele acompanha a Furia e qual jogador favorito.
