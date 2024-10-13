import logging
from telegram.ext import Updater, CommandHandler, MessageHandler
import aiohttp
import subprocess

logging.basicConfig(level=logging.INFO)

TOKEN = 'YOUR_API_TOKEN_HERE'

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Hello! I can record m3u8 streams.')

def record_stream(update, context):
    # Get the m3u8 URL from the user
    url = update.message.text.split(' ')[1]

    # Set the recording quality and duration
    quality = '1080p'  # You can change this to any quality you want
    duration = 60  # You can change this to any duration you want

    # Use ffmpeg to record the stream
    command = f'ffmpeg -i {url} -c:v libx264 -crf 18 -c:a aac -b:a 128k -f mpegts output.ts'
    subprocess.run(command, shell=True)

    # Upload the recorded video to Telegram
    with open('output.ts', 'rb') as f:
        context.bot.send_video(chat_id=update.effective_chat.id, video=f, timeout=100)

def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('record', record_stream))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
