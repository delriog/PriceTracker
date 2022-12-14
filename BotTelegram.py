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

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Olá, {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )
    update.message.reply_markdown_v2(
        fr'Para iniciar digite o comando /link e em seguida o link do produto desejado',
        reply_markup=ForceReply(selective=True),
    )



def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def link(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /link is issued."""
    update.message.reply_text("Estamos conferindo o seu produto!\n\nIsso pode levar alguns segundos!")
    link = update.message.text[6:]
    requestheaders = {
        "link": link
    }
    url = f"http://localhost:8080/produto"

    try: 
        dados = requests.get(url, headers=requestheaders)
        dados = dados.json()
        print("\n>>>>>>>>>>> dados: ", dados, "<<<<<<<<<<<<<<<\n")
    except : 
        update.message.reply_text("Produto nao encontrado")
        return



    resposta = "Produto com o nome: " + dados["titulo"] + "\nPreço: " + dados["preco"] + "\nFoi cadastrado com sucesso!!!"
    update.message.reply_text(resposta)


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


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

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()