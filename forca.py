import random
import os
from telegram import Update
from telegram.ext import CallbackContext

# Exemplo de palavras para o jogo da forca
palavras = ['futebol', 'campeonato', 'goleiro', 'torcida']

# Caminho para a pasta de imagens
IMAGEM_PATH = 'imagens_forca/'

# Função para iniciar o jogo da forca
async def forca(update: Update, context: CallbackContext):
    palavra = random.choice(palavras)
    context.user_data['forca_palavra'] = palavra
    context.user_data['forca_chutes'] = []
    context.user_data['forca_erros'] = 0

    masked_word = '_' * len(palavra)
    
    try:
        # Enviar a imagem inicial da forca
        image_path = os.path.join(IMAGEM_PATH, 'forca_7.png')
        with open(image_path, 'rb') as image_file:
            await update.message.reply_photo(photo=image_file, caption=f"🕹️ Jogo da Forca iniciado! Palavra: {masked_word}\nEnvie suas tentativas!")
        print("Jogo da forca iniciado com sucesso.")
    except Exception as e:
        print(f"Erro ao enviar a imagem ou mensagem: {e}")

# Função para processar as tentativas
async def tentar_forca(update: Update, context: CallbackContext):
    if 'forca_palavra' not in context.user_data:
        await update.message.reply_text("Inicie o jogo da forca com o comando /forca.")
        return

    palavra = context.user_data['forca_palavra']
    chutes = context.user_data['forca_chutes']
    erros = context.user_data['forca_erros']

    tentativa = update.message.text.lower()
    if tentativa in chutes:
        await update.message.reply_text("Você já tentou essa letra.")
        return

    chutes.append(tentativa)
    if tentativa in palavra:
        masked_word = ''.join([c if c in chutes else '_' for c in palavra])
        if '_' not in masked_word:
            await update.message.reply_text(f"Parabéns! Você acertou a palavra: {palavra}")
            del context.user_data['forca_palavra']
        else:
            # Atualizar a imagem com base no número de erros
            image_index = 7 - context.user_data['forca_erros']
            image_path = os.path.join(IMAGEM_PATH, f'forca_{image_index}.png')
            try:
                with open(image_path, 'rb') as image_file:
                    await update.message.reply_photo(photo=image_file, caption=f"Boa! Palavra: {masked_word}")
            except Exception as e:
                print(f"Erro ao enviar a imagem de progresso: {e}")
    else:
        erros += 1
        context.user_data['forca_erros'] = erros
        if erros >= 7:  # Número de erros permitido
            await update.message.reply_text(f"Game Over! A palavra era: {palavra}")
            # Enviar imagem final com a forca completa
            try:
                image_path = os.path.join(IMAGEM_PATH, 'forca_1.png')
                with open(image_path, 'rb') as image_file:
                    await update.message.reply_photo(photo=image_file, caption=f"Você perdeu o jogo! A palavra era: {palavra}")
            except Exception as e:
                print(f"Erro ao enviar a imagem final: {e}")
            del context.user_data['forca_palavra']
        else:
            # Atualizar imagem com o progresso da forca
            image_index = 7 - erros
            image_path = os.path.join(IMAGEM_PATH, f'forca_{image_index}.png')
            try:
                with open(image_path, 'rb') as image_file:
                    await update.message.reply_photo(photo=image_file, caption=f"Errado! Tente novamente. Erros: {erros}")
            except Exception as e:
                print(f"Erro ao enviar a imagem com erro: {e}")