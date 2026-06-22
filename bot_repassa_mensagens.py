"""
Bot do Telegram que copia (sem mostrar origem) todas as mensagens
de um Grupo 1 para um Grupo 2.

REQUISITOS:
    pip install python-telegram-bot --upgrade

COMO USAR:
1. Crie um bot com o @BotFather no Telegram e copie o TOKEN.
2. Adicione o bot no Grupo 1 e no Grupo 2.
3. Descubra o ID dos dois grupos (veja instruções no final deste arquivo).
4. Preencha as variáveis BOT_TOKEN, GRUPO_ORIGEM_ID e GRUPO_DESTINO_ID abaixo.
5. Execute: python bot_repassa_mensagens.py
"""

import logging
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

# ===================== CONFIGURAÇÃO =====================
BOT_TOKEN = "COLOQUE_SEU_TOKEN_AQUI"
GRUPO_ORIGEM_ID = -1001111111111   # ID do Grupo 1 (origem)
GRUPO_DESTINO_ID = -1002222222222  # ID do Grupo 2 (destino)
# ==========================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def copiar_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Copia a mensagem do Grupo 1 para o Grupo 2, sem indicar a origem."""
    chat_id = update.effective_chat.id

    # Só age se a mensagem vier do grupo de origem configurado
    if chat_id != GRUPO_ORIGEM_ID:
        return

    try:
        # copy_message envia uma cópia "limpa", sem mostrar de onde veio
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

    # filters.ALL captura texto, foto, vídeo, áudio, documento, sticker, etc.
    app.add_handler(MessageHandler(filters.ALL, copiar_mensagem))

    logger.info("Bot iniciado. Aguardando mensagens...")
    app.run_polling()


if __name__ == "__main__":
    main()

# ==========================================================
# COMO DESCOBRIR O ID DE UM GRUPO:
# 1. Adicione o bot @getidsbot (ou similar) no grupo,
#    ou
# 2. Envie uma mensagem qualquer no grupo e acesse:
#    https://api.telegram.org/bot<SEU_TOKEN>/getUpdates
#    Procure por "chat":{"id": -100..., ...} -> esse é o ID do grupo.
#    IDs de grupos/supergrupos são números negativos.
# ==========================================================
