from telegram import Update
from telegram.ext import CallbackContext

async def sorteio(update: Update, context: CallbackContext):
    chat_members = await context.bot.get_chat_members_count(update.message.chat_id)
    if chat_members < 2:
        await update.message.reply_text("Não há participantes suficientes para o sorteio.")
        return

    participants = [member.user.id for member in await context.bot.get_chat_administrators(update.message.chat_id)]
    if not participants:
        await update.message.reply_text("Nenhum participante encontrado para o sorteio.")
        return

    winner_id = choice(participants)
    winner = await context.bot.get_chat_member(update.message.chat_id, winner_id)
    await update.message.reply_text(f"🏆 O vencedor do sorteio é: {winner.user.full_name} (@{winner.user.username})")