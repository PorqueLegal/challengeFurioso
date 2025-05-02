# importar DB e interacoes
import os
import sqlite3
import logging

import requests
import aiohttp
from bs4 import BeautifulSoup

from telegram.helpers import escape_markdown

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    filters
)

from dotenv import load_dotenv
import os

# Carregar as variáveis do arquivo .env
load_dotenv()

# Obter o token do bot
TOKEN = os.getenv("BOTTOKEN")


# Estados da conversa
NAME, ALTERANDO_NOME, CALEND= range(3)

# --- Banco de Dados ---
def criar_banco():
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            telegram_id INTEGER PRIMARY KEY,
            nome TEXT
        )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS respostas (
        telegram_id INTEGER,
        pergunta TEXT,
        resposta TEXT
    )
    """)
    conn.commit()
    conn.close()


# salvar e recuperar dados
def salvar_usuario(telegram_id, nome):
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO usuarios (telegram_id, nome) VALUES (?, ?)", (telegram_id, nome))
    conn.commit()
    conn.close()

def buscar_nome(telegram_id):
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    c.execute("SELECT nome FROM usuarios WHERE telegram_id = ?", (telegram_id,))
    resultado = c.fetchone()
    conn.close()
    return resultado[0] if resultado else None


def salvar_resposta(telegram_id, pergunta, resposta):
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    c.execute("INSERT INTO respostas (telegram_id, pergunta, resposta) VALUES (?, ?, ?)", (telegram_id, pergunta, resposta))
    conn.commit()
    conn.close()

def buscar_respostas(telegram_id):
    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    c.execute("SELECT pergunta, resposta FROM respostas WHERE telegram_id = ?", (telegram_id,))
    resultados = c.fetchall()
    conn.close()
    return resultados


# Função para acessar sites
async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                return None




# --- Conversa---
# Inicio
# nome
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    nome = buscar_nome(telegram_id)

    if nome:
        await update.message.reply_text(f"👋 Olá novamente, {nome}! \n\n📌Digite /menu para ver as opçoes\n\n ❔ Digite /help caso tenha duvidas sobre comandos")
    else:
        await update.message.reply_text("👋 'Olá! Eu sou o assistente da FURIA, estou aqui para te ajudar na sua jornada pra se torna um fã da Furia CS, por tanto vou precisar de algumas informações pra criar um cadastro seu. Por isso, digite seu nome:")
        return NAME

async def receber_nome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nome = update.message.text.strip()
    telegram_id = update.effective_user.id
    salvar_usuario(telegram_id, nome)
    await update.message.reply_text(f"✅ Nome: {nome}\n\n 📌 Use /menu para interagir \n\n❔ Duvidas sobre comandos /help")
    return ConversationHandler.END



# MUDA NOME
async def mudarNome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✏️ 'Mude seu nome:'")
    return ALTERANDO_NOME

async def alterar_nome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    novo_nome = update.message.text
    telegram_id = update.effective_user.id

    conn = sqlite3.connect("usuarios.db")
    c = conn.cursor()
    c.execute("UPDATE usuarios SET nome = ? WHERE telegram_id = ?", (novo_nome, telegram_id))
    conn.commit()
    conn.close()

    await update.message.reply_text(f"✅ Seu nome foi atualizado para *{novo_nome}*.", parse_mode="Markdown")
    return ConversationHandler.END






# COMANDOS
async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Ação cancelada.")
    return ConversationHandler.END

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('⚙ Comandos disponíveis:\n\n  ▶ Inicia o bot /start\n\n 📌 Use /menu para interagir \n\n 📋 Ver dados /dados \n\n ✏️ Mudar o nome /mudarNome \n\n ❔ Duvidas sobre comandos /help')
    return ConversationHandler.END

async def dados(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    nome = buscar_nome(telegram_id)
    await update.message.reply_text(f"👤 Seu nome: {nome}! ")





# --- Opcoes ---
async def menu (update: Update, context: ContextTypes.DEFAULT_TYPE):
    botoes = [
        [InlineKeyboardButton("🗓 Campeonatos", callback_data="Campeonatos")],
        [InlineKeyboardButton("🎮 Jogadores", callback_data="players")],
        [InlineKeyboardButton("🤳 Notícias", callback_data="news")],
         [InlineKeyboardButton("📱 Redes Sociais", callback_data="redes")]
    ]
    markup = InlineKeyboardMarkup(botoes)
    await update.message.reply_text("📋 Menu Principal:\n Escolha uma opção:", reply_markup=markup)





#as escolhas das opcoes
async def responder_botao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()


#Campeonatos 
    if query.data == "Campeonatos":
        botoes = [  
            [InlineKeyboardButton("↩ Voltar", callback_data="voltar_menu")]
        ]
        await query.edit_message_text("🗓  Jogos: \n\n ▫ PGL Astana 2025: 10/05/25 à 18/05/25 \n\n ▫ IEM Dallas 2025: 19/05/25 à 25/05/25\n\n ▫ BLAST.tv Austin Major 2025: 03/06/25 à 22/06/25",
            reply_markup=InlineKeyboardMarkup(botoes),
            parse_mode="Markdown"
        )  
      
      
        # URL e requisição
        # url = "https://draft5.gg/equipe/330-FURIA"
        # response = requests.get(url)

        # if response.status_code == 200:
        #     soup = BeautifulSoup(response.content, "html.parser")

        #     # Encontrar os elementos desejados
        #     elementos = soup.find_all("div", class_="sc-dkPtRN jLjnJq", limit=1)

        #     if elementos:
        #         # Processar os elementos encontrados
        #         texto_elementos = "\n".join([el.text.strip() for el in elementos])
        #         await query.edit_message_text(
        #             f"🗓  Jogos: \n\n"
        #             f"▫ PGL Astana 2025: 10/05/25 à 18/05/25 \n\n"
        #             f"▫ IEM Dallas 2025: 19/05/25 à 25/05/25\n\n"
        #             f"▫ BLAST.tv Austin Major 2025: 03/06/25 à 22/06/25\n\n"
        #             f"🏆 Campeonatos Recentes: \n\n{texto_elementos}"
        #         )
        #     else:
        #         await query.edit_message_text(
        #             "Elemento não encontrado na página."
        #         )
        # else:
        #     await query.edit_message_text(
        #         "Erro ao acessar a página."
        #     )






# players
    elif query.data == "players":
        botoes = [
            [InlineKeyboardButton(" 🇧🇷 FalleN", callback_data="FalleN")],
            [InlineKeyboardButton(" 🇧🇷 KSCERATO", callback_data="KSCERATO")],
            [InlineKeyboardButton(" 🇧🇷 yuurih", callback_data="yuurih")],
            [InlineKeyboardButton(" 🇰🇿 MOLODOY", callback_data="MOLODOY")],
            [InlineKeyboardButton(" 🇱🇻 YEKINDAR", callback_data="YEKINDAR")],
    
            [InlineKeyboardButton("↩ Voltar", callback_data="voltar_menu")]
        ]
        await query.edit_message_text("🎮 Jogadores:", reply_markup=InlineKeyboardMarkup(botoes))
   

        botoes = [
            [InlineKeyboardButton("↩ Voltar", callback_data="voltar_menu")]
        ]


    elif query.data == "FalleN":
        botoes = [
            [InlineKeyboardButton("↩ Voltar", callback_data="voltar_menu")]
        ]
        await query.edit_message_text("🇧🇷  FalleN: \n\n ▫ Nome: Gabriel Toledo de Alcântara Sguario \n\n ▫ Nacionalidade: 🇧🇷 Brasil \n\n ▫ Funções: In-game leader AWPer",
            reply_markup=InlineKeyboardMarkup(botoes),
            parse_mode="Markdown"
        )  

    elif query.data == "KSCERATO":
        botoes = [
            [InlineKeyboardButton("↩ Voltar", callback_data="voltar_menu")]
        ]
        await query.edit_message_text("🇧🇷  KSCERATO: \n\n ▫ Nome: Kaike Silva Cerato \n\n ▫ Nacionalidade: 🇧🇷 Brasil \n\n ▫ Funções: Rifler (lurker)",
            reply_markup=InlineKeyboardMarkup(botoes),
            parse_mode="Markdown"
        )  
        

    elif query.data == "yuurih":
        botoes = [
            [InlineKeyboardButton("↩ Voltar", callback_data="voltar_menu")]
        ]    

        await query.edit_message_text("🇧🇷  yuurih: \n\n ▫ Nome: Yuri Gomes dos Santos Boian \n\n ▫ Nacionalidade: 🇧🇷 Brasil \n\n ▫ Funções: Rifler",
            reply_markup=InlineKeyboardMarkup(botoes),
            parse_mode="Markdown"
        )  
        
       
    
    elif query.data == "MOLODOY":
        botoes = [
            [InlineKeyboardButton("↩ Voltar", callback_data="voltar_menu")]
        ]     

        await query.edit_message_text("🇰🇿 MOLODOY: \n\n ▫ Nome:  Данил Голубенко (Danil Golubenko) \n\n ▫ Nacionalidade: 🇰🇿 Cazaquistão \n\n ▫ Funções: AWPer",
            reply_markup=InlineKeyboardMarkup(botoes),
            parse_mode="Markdown"
        ) 

       

    elif query.data == "YEKINDAR":
        botoes = [
            [InlineKeyboardButton("↩ Voltar", callback_data="voltar_menu")]
        ]  
        
        await query.edit_message_text("🇱🇻 YEKINDAR: \n\n ▫ Nome:  Mareks Gaļinskis \n\n ▫ Nacionalidade: 🇱🇻 Letônia \n\n ▫ Funções: Rifler (entry fragger)",
            reply_markup=InlineKeyboardMarkup(botoes),
            parse_mode="Markdown"
        ) 
         






#    noticias
    elif query.data == "news":
        url = "https://draft5.gg/equipe/330-FURIA"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        # Fazer o parse do HTML com BeautifulSoup
                        soup = BeautifulSoup(await response.text(), "html.parser")
                        
                        # Encontrar todas as manchetes
                        manchetes = soup.find_all(
                            "a", 
                            class_="NewsCardSmall__NewsCardSmallContainer-sc-1q3y6t7-0 fJEICo", 
                            limit=3
                        )
                        
                        # Criar uma lista de links formatados
                        noticias = [
                            f"[{manchete.text.strip()}](https://draft5.gg{manchete['href']})"
                            for manchete in manchetes if manchete.has_attr('href')
                        ]
                        
                        # Montar a mensagem com as notícias formatadas
                        mensagem = "\n\n".join(noticias) if noticias else "Nenhuma notícia disponível."
                    else:
                        mensagem = f"Erro ao acessar o site. Código HTTP: {response.status}"
        except Exception as e:
            mensagem = f"Erro ao buscar notícias: {str(e)}"


        botoes = [
            [InlineKeyboardButton("↩ Voltar", callback_data="voltar_menu")]
        ]
        
        # Enviar a mensagem formatada como links clicáveis e botões
        await query.edit_message_text(
            text=f"🤳 **Notícias Recentes:**\n\n{mensagem}",
            reply_markup=InlineKeyboardMarkup(botoes),
            parse_mode="Markdown"
        )





# redes sociais
    elif query.data == "redes":
        botoes = [
            [InlineKeyboardButton("🌐 Site",  url="https://www.furia.gg")], 
            [InlineKeyboardButton("📷 Instagram",  url="https://www.instagram.com/furiagg/")],
            [InlineKeyboardButton("✖ X",  url="https://x.com/FURIA")],
            [InlineKeyboardButton("↩ Voltar", callback_data="voltar_menu")]
        ]
        await query.edit_message_text("🎮 Redes sociais:", reply_markup=InlineKeyboardMarkup(botoes))




    # voltar menu
    # elif query.data == "voltar_menu":
    #     await menu(query, context)


    # voltar menu
    elif query.data == "voltar_menu":
        await menu(query, update)





# --- Cria o banco de dados local se ainda não existir
# Define os comandos e conversas que o bot reconhece 
# Inicia o bot com run_polling()

def main():
    criar_banco()
    app = ApplicationBuilder().token(TOKEN).build()

    conversa = ConversationHandler(
        entry_points=[CommandHandler("start", start),
                    CommandHandler("mudarNome", mudarNome),
                    ],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_nome)],
            ALTERANDO_NOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, alterar_nome)],
        },
        fallbacks=[CommandHandler("cancelar", cancelar)],
    )

    app.add_handler(conversa)
    app.add_handler(CommandHandler("dados", dados))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(responder_botao))


    print("🤖 Bot com banco de dados e perguntas personalizadas rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()
