import logging
import os.path
import json
import aiofiles
from telegram import Update
from telegram.ext import CallbackContext

# Configuração do logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Carregar pontos dos usuários
async def load_points():
    if os.path.isfile('pontos.json'):
        async with aiofiles.open('pontos.json', 'r', encoding='utf-8') as file:
            points = json.loads(await file.read())
            logger.info("Pontos carregados com sucesso.")
            return points
    else:
        logger.info("Arquivo de pontos não encontrado, criando novo.")
        return {}

# Função para mostrar o ranking
async def tabela(update: Update, context: CallbackContext):
    user_points = await load_points()  # Carregar os pontos aqui
    if not user_points:
        await update.message.reply_text("📉 A tabela está vazia. Comece a jogar e acumule pontos!")
        return

    sorted_users = sorted(user_points.items(), key=lambda x: x[1], reverse=True)
    ranking_message = "🏆 **Ranking Atual**\n\n"
    user_names = {}  # Dicionário para armazenar nomes

    for user_id, points in sorted_users:
        if user_id not in user_names:
            try:
                user = await context.bot.get_chat_member(chat_id=update.message.chat_id, user_id=int(user_id))
                if user.user.username:
                    display_name = f"@{user.user.username}"
                else:
                    display_name = user.user.full_name
                user_names[user_id] = display_name
            except Exception as e:
                logger.error(f"Erro ao obter informações do usuário {user_id}: {e}")
                user_names[user_id] = "Desconhecido"

    for idx, (user_id, points) in enumerate(sorted_users, start=1):
        display_name = user_names[user_id]
        ranking_message += f"**{idx}. {display_name}** - {points} pontos\n"

    await update.message.reply_text(ranking_message, parse_mode='Markdown')