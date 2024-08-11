# main.py

from telegram.ext import Updater, CommandHandler
from commands import generate
import os

def main():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler('generate', generate))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
