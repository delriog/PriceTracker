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

def get_chat_id(self, message):
        '''
        Telegram chat type can be either "private", "group", "supergroup" or
        "channel".
        Return user ID if it is of type "private", chat ID otherwise.
        '''
        if message.chat.type == 'private':
            return message.user.id

        return message.chat.id

# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Bem vindo ao bot de produtos do site AMAZON\n\nPara cadastrar um produto da amazon digite /link <link do produto da amazon>\n\nPara verificar produtos cadastrados digite /produtos')



def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    if update.message.chat.type == 'private':
        telegram_id = update.message.from_user.id
        print(telegram_id)
    update.message.reply_text('Para cadastrar um produto da amazon digite /link <link do produto da amazon>\n\nPara verificar produtos cadastrados digite /produtos')


def produtos(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /produtos is issued."""
    if update.message.chat.type == 'private':
        telegram_id = str(update.message.from_user.id)
    else:
        update.message.reply_text("Bot não disponível para o seu tipo de chat")
        return

    
    requestheaders = {
        "id": telegram_id
    }


    url = f"http://localhost:8080/retornaprodutos"
    verifica = requests.get(url, headers=requestheaders)
    verifica = verifica.json()
    print("type>", type(verifica))
    if not verifica:
        update.message.reply_text("Não há produtos cadastrados\n\n")
        return
    update.message.reply_text("Lista de produtos cadastrados:\n\n")
    for nome, preco in verifica:
        resposta = "\nProduto: " + nome + "\ncom o preço: " + str(preco)
        update.message.reply_text(resposta)


def link(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /link is issued."""
    update.message.reply_text("Estamos conferindo o seu produto!\n \nIsso pode levar alguns segundos!")
    link = update.message.text[6:]
    if update.message.chat.type == 'private':
        telegram_id = str(update.message.from_user.id)
    else:
        update.message.reply_text("Bot não disponível para o seu tipo de chat")
        return
    requestheaders = {
        "link": link,
        "id": telegram_id
    }
    url = f"http://localhost:8080/verificaproduto"
    verifica = requests.get(url, headers=requestheaders)
    verifica = verifica.json()
    if verifica["resposta"] == "ok":
        pass
    else:
        resposta = "Produto ja cadastrado anteriormente, digite /produtos para listar os produtos cadastrados"
        update.message.reply_text(resposta)
        return

    url = f"http://localhost:8080/cadastraproduto"

    try: 
        dados = requests.get(url, headers=requestheaders)
        dados = dados.json()
    except : 
        update.message.reply_text("Produto nao encontrado")
        return

    resposta = "Produto com o nome: " + dados["titulo"] + "\nPreço: " + dados["preco"] + "\nFoi cadastrado com sucesso!!!"
    update.message.reply_text(resposta)


# def echo(update: Update, context: CallbackContext) -> None:
#     """Echo the user message."""
#     update.message.reply_text(update.message.text)


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