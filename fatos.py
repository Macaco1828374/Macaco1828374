import logging
import random
from telegram import Update
from telegram.ext import CallbackContext

# Configuração do logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Função para carregar fatos de um arquivo
def carregar_fatos(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            fatos = file.readlines()
        # Remove quebras de linha e espaços extras
        return [fato.strip() for fato in fatos if fato.strip()]
    except Exception as e:
        logger.error(f"Erro ao carregar fatos: {e}")
        return []

# Função para exibir fatos curiosos
async def fatos(update: Update, context: CallbackContext):
    fatos = carregar_fatos('fatos.txt')
    
    if not fatos:
        await update.message.reply_text("📚 Não consegui encontrar fatos curiosos no momento.")
        return
    
    fato = random.choice(fatos)
    await update.message.reply_text(f"📚 Fato curioso:\n{fato}")