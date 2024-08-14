import os
import json
import time
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from random import choice
import logging
from datetime import datetime

# Importar os comandos dos arquivos
from start import start
from tabela import tabela
from fatos import fatos
from sorteio import sorteio  # Novo comando
from forca import forca, tentar_forca  # Novo comando

# Configuração do logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Caminho para o arquivo de pontos
POINTS_FILE = 'pontos.json'
RESPONSES_FILE = 'respostas.txt'

# Carregar perguntas de um arquivo
def load_questions(file_path):
    questions = {}
    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if ':' in line:
                    question, answer = line.strip().split(':', 1)
                    questions[question] = answer
    return questions

# Carregar respostas alternativas de um arquivo .txt
def load_responses(file_path):
    responses = {}
    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if ':' in line:
                    question, answer = line.strip().split(':', 1)
                    responses[question] = [ans.strip() for ans in answer.split(',')]
    return responses

# Carregar pontos dos usuários
def load_points():
    if os.path.isfile(POINTS_FILE):
        with open(POINTS_FILE, 'r', encoding='utf-8') as file:
            points = json.load(file)
            logger.info("Pontos carregados com sucesso.")
            return points
    else:
        logger.info("Arquivo de pontos não encontrado, criando novo.")
        return {}

# Salvar pontos dos usuários
def save_points(points):
    with open(POINTS_FILE, 'w', encoding='utf-8') as file:
        json.dump(points, file, ensure_ascii=False, indent=4)
        logger.info("Pontos salvos com sucesso.")

questions = load_questions('perguntas.txt')
questions_list = list(questions.keys())
responses = load_responses(RESPONSES_FILE)  # Obtém as respostas alternativas

# Inicializar o sistema de pontos
user_points = load_points()

# Função para enviar uma nova pergunta
async def enviar_pergunta(context: CallbackContext):
    if not questions_list:
        return  # Não faz nada se não houver perguntas

    question = choice(questions_list)
    context.bot_data['current_question'] = question
    context.bot_data['answer'] = questions[question]
    context.bot_data['question_time'] = time.time()  # Registra o tempo da pergunta

    chat_id = context.job.chat_id
    sent_message = await context.bot.send_message(chat_id=chat_id, text=f"Macaco")
    context.bot_data['question_message_id'] = sent_message.message_id  # Guarda o ID da mensagem da pergunta

# Função para verificar a resposta
async def resposta(update: Update, context: CallbackContext):
    if 'current_question' not in context.bot_data:
        return  # Não faz nada se não houver pergunta ativa

    if update.message.reply_to_message and update.message.reply_to_message.message_id == context.bot_data['question_message_id']:
        user_answer = update.message.text.lower()
        correct_answer = context.bot_data['answer'].lower()
        question_time = context.bot_data['question_time']
        response_time = time.time() - question_time

        # Verifica se a resposta do usuário está na lista de respostas alternativas
        if user_answer in [ans.lower() for ans in responses.get(context.bot_data['current_question'], [])] or user_answer == correct_answer:
            user_id = str(update.message.from_user.id)  # Armazenar user_id como string para garantir compatibilidade JSON
            base_points = 10
            # Aumenta a quantidade de pontos com base na rapidez da resposta
            points_earned = max(1, base_points - int(response_time))  # Garante no mínimo 1 ponto
            if user_id not in user_points:
                user_points[user_id] = 0
            user_points[user_id] += points_earned
            save_points(user_points)  # Salvar pontos atualizados
            await update.message.reply_text(f"🎉 Acertou! Você ganhou {points_earned} ponto(s)!")
            del context.bot_data['current_question']
            del context.bot_data['answer']
            del context.bot_data['question_time']
            del context.bot_data['question_message_id']
        else:
            await update.message.reply_text("❌ Resposta incorreta. Tente novamente!")

# Função para ler piadas do arquivo
def load_jokes(file_path='piadas.txt'):
    with open(file_path, 'r', encoding='utf-8') as file:
        jokes = file.readlines()
    return [joke.strip() for joke in jokes]

jokes = load_jokes()

# Função para enviar uma piada aleatória
async def piada(update: Update, context: CallbackContext):
    joke = choice(jokes)
    await update.message.reply_text(joke)

# Função para calcular a contagem regressiva
async def contagem(update: Update, context: CallbackContext):
    if len(context.args) < 2:
        await update.message.reply_text("Por favor, use o formato: /contagem [evento] [data (dd-mm-yyyy)]")
        return

    event = context.args[0]
    try:
        event_date = datetime.strptime(context.args[1], '%d-%m-%Y')
        now = datetime.now()
        delta = event_date - now
        if delta.days < 0:
            await update.message.reply_text(f"O evento {event} já passou!")
        else:
            await update.message.reply_text(f"Faltam {delta.days} dias para o evento {event}.")
    except ValueError:
        await update.message.reply_text("Formato de data inválido. Use o formato: dd-mm-yyyy")

# Função para ler times do arquivo
def load_teams(file_path='times.txt'):
    with open(file_path, 'r', encoding='utf-8') as file:
        teams = file.readlines()
    return [team.strip() for team in teams]

teams = load_teams()

# Função para gerar times aleatórios
async def time(update: Update, context: CallbackContext):
    if len(context.args) != 1 or not context.args[0].isdigit() or int(context.args[0]) > 2:
        await update.message.reply_text("Use o formato: /time [Quantidade] (Max 2)")
        return

    num_teams = int(context.args[0])
    selected_teams = []
    while len(selected_teams) < num_teams:
        team = choice(teams)
        if team not in selected_teams:
            selected_teams.append(team)
    response = "\n".join(selected_teams)
    await update.message.reply_text(f"Times selecionados:\n{response}")

def main():
    # Substitua pelo token real do seu bot
    bot_token = "6607713315:AAEUn9KT4ry8ei78niJ6Rph-gIzxX2okFIU"
    chat_id = "-1002220497046"

    application = Application.builder().token(bot_token).build()

    # Adiciona os handlers
    application.add_handler(CommandHandler("tabela", tabela))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("fatos", fatos))
    application.add_handler(CommandHandler("piada", piada))
    application.add_handler(CommandHandler("contagem", contagem))
    application.add_handler(CommandHandler("time", time))
    application.add_handler(CommandHandler("sorteio", sorteio))  # Novo comando
    application.add_handler(CommandHandler("forca", forca))  # Novo comando
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, resposta))

    # Adiciona JobQueue para enviar perguntas a cada 30 minutos
    job_queue = application.job_queue
    job_queue.run_repeating(enviar_pergunta, interval=1800, first=10, chat_id=chat_id)  # Intervalo de 30 minutos

    # Correção: Use asyncio.run() para iniciar o loop do evento
    asyncio.run(application.run_polling())

if __name__ == '__main__':
    main()