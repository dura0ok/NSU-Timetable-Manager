import logging
import requests

from dotenv import load_dotenv
from telegram import Update, File
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, DictPersistence, MessageHandler, filters, ConversationHandler

from config_parser import ConfigParser

load_dotenv()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

httpx_logger = logging.getLogger('httpx')
httpx_logger.setLevel(logging.WARNING)


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


async def downloader(update, context):
    file: File = await context.bot.get_file(update.message.document)
    path: str = file.file_path

    r = requests.get(path)
    print(r.json())


if __name__ == "__main__":
    try:
        app = ApplicationBuilder().token(ConfigParser.parse_bot_token()).build()
        print(type(app))
        app.add_handler(CommandHandler("start", hello))
        app.add_handler(MessageHandler(filters.Document.ALL, downloader))
        app.run_polling()
        app.run_webhook()
    except KeyError as e:
        logger.exception("Key Error : " + str(e))
