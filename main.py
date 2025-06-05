from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters
import os

from processor_pdf import process_file
from processor_jpg import process_file_jpg

TOKEN = '7430434597:AAGhxYjbdzJOaew-ooqFHvlp4HPyL9fgrcE'
MAX_MESSAGE_LENGTH = 4096


def split_message(text):
    return [text[i:i+MAX_MESSAGE_LENGTH] for i in range(0, len(text), MAX_MESSAGE_LENGTH)]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Пришлите pdf или jpg файл с таблицей, соответствующей формату.')


async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    if document.mime_type != 'application/pdf':
        await update.message.reply_text('Формат файла не поддерживается')
        return

    file = await context.bot.get_file(document.file_id)
    await file.download_to_drive(document.file_name)

    try:
        json_string = process_file(document.file_name)
        for part in split_message(json_string):
            await update.message.reply_text(part)
    except Exception as e:
        await update.message.reply_text(f'Ошибка при обработке файла: {e}')
    finally:
        try:
            os.remove(document.file_name)
        except Exception:
            pass


async def handle_jpg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = None
    filename = ''
    if update.message.photo:
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        filename = 'photo.jpg'
    else:
        document = update.message.document
        if document.mime_type != 'image/jpeg':
            await update.message.reply_text('Формат файла не поддерживается')
            return

        file = await context.bot.get_file(document.file_id)
        filename = document.file_name
    await file.download_to_drive(filename)

    try:
        json_string = process_file_jpg(filename)
        await update.message.reply_text(json_string)
    except Exception as e:
        await update.message.reply_text(f'Ошибка при обработке файла: {e}')
    finally:
        try:
            os.remove(filename)
        except Exception:
            pass


if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.Document.PDF, handle_pdf))
    app.add_handler(MessageHandler(filters.Document.JPG, handle_jpg))
    app.add_handler(MessageHandler(filters.Document.IMAGE, handle_jpg))
    app.add_handler(MessageHandler(filters.PHOTO, handle_jpg))
    app.run_polling()
