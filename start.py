import logging
from telegram import Update
from telegram.ext import CallbackContext

# Configuração do logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext):
    welcome_message = (
        "👋 Olá! Eu sou o seu bot de Entretenimento Aqui estão alguns comandos que você pode usar:\n\n"
        "🏆 | /tabela - Mostra o ranking atual dos jogadores.\n"
        "📚 | /fatos - Mostra fatos curiosos sobre futebol.\n"
        "😂 | /piada - Envia uma piada aleatória\n"
        "📅 | /contagem - Faz a contagem regressiva para um evento especificado.\n"
        "⚽ | /time Gera um ou dois times aleatórios do mundo inteiro.\n\n"
        "Divirta-se! 🥳"
    )
    await update.message.reply_text(welcome_message, parse_mode='Markdown')