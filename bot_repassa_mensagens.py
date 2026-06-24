import os
import logging
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

BOT_TOKEN = os.environ["BOT_TOKEN"]
GRUPO_ORIGEM_ID = int(os.environ["GRUPO_ORIGEM_ID"])
GRUPO_DESTINO_ID = int(os.environ["GRUPO_DESTINO_ID"])

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def copiar_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    if chat_id != GRUPO_ORIGEM_ID:
        return
    try:
        await context.bot.copy_message(
            chat_id=GRUPO_DESTINO_ID,
            from_chat_id=chat_id,
            message_id=update.effective_message.message_id,
        )
        logger.info("Mensagem copiada do Grupo 1 para o Grupo 2.")
    except Exception as e:
        logger.error(f"Erro ao copiar mensagem: {e}")


def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, copiar_mensagem))
    logger.info("Bot iniciado. Aguardando mensagens...")
    app.run_polling()


if __name__ == "__main__":
    main()
