#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
import json

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def get_chat_id(self, message): # Function to get the chat id from the user that sent the message
        '''
        Telegram chat type can be either "private", "group", "supergroup" or
        "channel".
        Return user ID if it is of type "private", chat ID otherwise.
        '''
        if message.chat.type == 'private':
            return message.user.id

        return message.chat.id

# Funcction that display the first message
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Bem vindo ao bot de produtos do site AMAZON\n\nPara cadastrar um produto da amazon digite /link <link do produto da amazon>\n\nPara verificar produtos cadastrados digite /produtos')


# Function that show the help options
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    if update.message.chat.type == 'private':
        telegram_id = update.message.from_user.id
        print(telegram_id)
    update.message.reply_text('Para cadastrar um produto da amazon digite /link <link do produto da amazon>\n\nPara verificar produtos cadastrados digite /produtos')

# Function that returns a list of the registered products
def produtos(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /produtos is issued."""

    if update.message.chat.type == 'private': # Search for the user chat id
        telegram_id = str(update.message.from_user.id)

    else:
        update.message.reply_text("Bot não disponível para o seu tipo de chat")
        return

    
    requestheaders = {
        "id": telegram_id
    }

    url = f"http://localhost:8080/retornaprodutos" # Endpoint that will handle the requisition

    verifica = requests.get(url, headers=requestheaders) # Calls the endpoint
    verifica = verifica.json()
    produtos = verifica["produtos"] # A list of the registeres products
    produtos_atualizados = verifica["descontos"] # A list of the products that have discount

    if not verifica: # If doesnt have any registered products
        update.message.reply_text("Não há produtos cadastrados\n\n")
        return

    update.message.reply_text("Lista de produtos cadastrados:\n\n") # Display the registered products

    for nome, preco, link in produtos:
        for links in produtos_atualizados:
            if link == links:
                update.message.reply_text("Produto com desconto:") # If the product had discount
        resposta = "\nProduto: " + nome + "\ncom o preço: " + str(preco)
        update.message.reply_text(resposta)


def link(update: Update, context: CallbackContext) -> None: # Function that register a new product
    """Send a message when the command /link is issued."""

    update.message.reply_text("Estamos conferindo o seu produto!\n \nIsso pode levar alguns segundos!")

    link = update.message.text[6:]

    if update.message.chat.type == 'private':
        telegram_id = str(update.message.from_user.id)

    else:
        update.message.reply_text("Bot não disponível para o seu tipo de chat")
        return

    requestheaders = { # Header with the link and user chat id
        "link": link,
        "id": telegram_id
    }

    url = f"http://localhost:8080/verificaproduto" # Endpoint that verify the product

    verifica = requests.get(url, headers=requestheaders) # Calss the endpoint
    verifica = verifica.json()

    if verifica["resposta"] == "ok": # If the product is not registered
        pass
    else:
        resposta = "Produto ja cadastrado anteriormente, digite /produtos para listar os produtos cadastrados"
        update.message.reply_text(resposta)
        return

    url = f"http://localhost:8080/cadastraproduto" # Endpoint that register the products

    try: 
        dados = requests.get(url, headers=requestheaders) # Calss the endpoint
        dados = dados.json()
    except : 
        update.message.reply_text("Produto nao encontrado") 
        return

    resposta = "Produto com o nome: " + dados["titulo"] + "\nPreço: " + dados["preco"] + "\nFoi cadastrado com sucesso!!!" # Format the answer
    update.message.reply_text(resposta)




def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5789794783:AAF_sOuPbFyoZ7L7F9kRv24pW17l1xjjkCY")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("link", link))
    dispatcher.add_handler(CommandHandler("produtos", produtos))

    # on non command i.e message - echo the message on Telegram
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()