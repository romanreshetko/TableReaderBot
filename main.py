from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters
import os

from processor_pdf import process_file
from processor_jpg import process_file_jpg

TOKEN = '7430434597:AAGhxYjbdzJOaew-ooqFHvlp4HPyL9fgrcE'


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
        await update.message.reply_text(json_string)
    except Exception as e:
        await update.message.reply_text(f'Ошибка при обработке файла: {e}')
    finally:
        try:
            os.remove(document.file_name)
        except Exception:
            pass


async def handle_jpg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    if document.mime_type != 'image/jpeg':
        await update.message.reply_text('Формат файла не поддерживается')
        return

    file = await context.bot.get_file(document.file_id)
    await file.download_to_drive(document.file_name)

    try:
        json_string = process_file_jpg(document.file_name)
        await update.message.reply_text(json_string)
    except Exception as e:
        await update.message.reply_text(f'Ошибка при обработке файла: {e}')
    finally:
        try:
            os.remove(document.file_name)
        except Exception:
            pass


if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.Document.PDF, handle_pdf))
    app.add_handler(MessageHandler(filters.Document.JPG, handle_jpg))
    app.run_polling()
