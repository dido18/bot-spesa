from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import ParseMode
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

token = "1152313606:AAFmwRBXvksOV5W2QA7rWZcnNqy4p7zBKqA"

updater = Updater(token=token, use_context=True)

dispatcher = updater.dispatcher

list_items = None

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm you Corona Grocery bot, please talk to me!")

def new_list(update, context):
    global list_items
    if list_items is not None:
        context.bot.send_message(chat_id=update.effective_chat.id,  text="A grocery list is alredy present.")
    else:
        list_items = []
        context.bot.send_message(chat_id=update.effective_chat.id,  text="Grocery list created succesfully.")

def show_list(update, context):
    message = ""
    if list_items is None:
        message += "No list created."
    elif len(list_items) == 0:
        message += "Empty list"
    else:
        for i in list_items:
            message = message +  i + "\n"
    update.message.reply_text(message)

def clear_list(update, context):
    global list_items
    list_items = None
    update.message.reply_text("List cleared correctly.")

def add_item(update, context):
    message = ""
    if list_items is None:
        message += "No list created."
    else:
        logging.info("{} added correctly".format(context.args[0]))
        list_items.append(context.args[0])

        if len(list_items) == 0:
            message += "Lista vuota"
        else:
            for i in list_items:
                message = message +  i + "\n"
    update.message.reply_text(message)

def delete_item(update, context):
    message = ""
    if list_items is None:
        message += "No list created."
    else:
        list_items.remove(context.args[0])
        logging.info("{} removed correctly".format(context.args[0]))


        if len(list_items) == 0:
            message += "Lista vuota"
        else:
            for i in list_items:
                message = message +  i + "\n"
    update.message.reply_text(message)

def help_message(update, context):
    logging.info("Help message")
    message = "*Corona Python Grocery List:* \n"
    commands = [
        "/new - Create a new grocery",
        "/add Element - Add a new element into the grocery",
        "/del Element - Delete the element form the grocery",
        "/show - Show the current grocery",
        "/clear - Delete the grocery",
        "/help - Show this message",
    ]
    message += "\n".join(commands)
    update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)

new_handler = CommandHandler('new', new_list)
add_handler = CommandHandler("add", add_item)
delete_handler = CommandHandler("del", delete_item)
show_handler = CommandHandler("show", show_list)
clear_handler = CommandHandler("clear", clear_list)
help_handler = CommandHandler("help", help_message)

dispatcher.add_handler(new_handler)
dispatcher.add_handler(add_handler)
dispatcher.add_handler(delete_handler)
dispatcher.add_handler(show_handler)
dispatcher.add_handler(clear_handler)
dispatcher.add_handler(help_handler)

updater.start_polling()

updater.idle()