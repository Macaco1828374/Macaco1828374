import random
from telegram import Update
from telegram.ext import CallbackContext

# Função para ler piadas do arquivo
def load_jokes(file_path='piadas.txt'):
    with open(file_path, 'r', encoding='utf-8') as file:
        jokes = file.readlines()
    return [joke.strip() for joke in jokes]

jokes = load_jokes()

# Função para enviar uma piada aleatória
async def piada(update: Update, context: CallbackContext):
    joke = random.choice(jokes)
    await update.message.reply_text(joke)