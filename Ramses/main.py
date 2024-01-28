from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

TOKEN: Final = '6818698464:AAExduA8qUwEWa3wl1i_M2gK3OVF2Uv0-Fk'
BOT_USERNAME: Final = '@EunaiBot'
NAME, ID_NUMBER = range(2)
#Arrays
commands = [
    ('/start', 'Intializes the bot'), ('/help', 'Lists all known commands'), ('/status', 'Provides your current health status'), 
    ('/register', 'Intiates registration process'), ('regCancel', 'Cancels the registration process'),

]

#Misc functions, formatting etc
def format_help_command(commands):
    return '\n'.join([f'{command}: {description}' for command, description in commands])

#Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello!, I am Eunai. How can I help you today?\n')
    await update.message.reply_text('Please use the /register command to link Eunai with your data')
    await update.message.reply_text('Type /help for the list of known commands.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands_list = format_help_command(commands)
    help_message = ('Here are the list of commands I know')
    await update.message.reply_text(help_message)
    await update.message.reply_text(commands_list)
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Custom Command')

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    intro = ('Please wait while I pull your data')
    await update.message.reply_text(intro)
    
#Registration command, and linking with convo handler
async def register_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Beginning registration process')
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.text
    context.user_data['name'] = user_name
    await update.message.reply_text(f'Thank you {user_name}. Please enter your ID NUMBER assigned by the Space Health Ministry:')
    return ID_NUMBER

async def get_id_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.text
    context.user_data['id_number'] = user_id
    completion_msg = f'Registration is now complete.\nVerify your information. If you need to make changes, re-initiate the registration process' 
    userId_msg = f'\n Username: {context.user_data["name"]}\nID_Number: {user_id}'
    await update.message.reply_text(completion_msg)
    await update.message.reply_text(userId_msg)
    return ConversationHandler.END

async def regCancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Registration has been cancelled...\nComplete registration to continue using Eunai')
    return ConversationHandler.END #ends convo
#Responses 
def handle_response(text: str) -> str:
    processed: str = text.lower()
    if 'hello' in processed:
        return 'hello there!'
    if 'help' in processed:
        return 'use the command for help'
    
    return 'I dont understand... please use the help command'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    #group or private chat
    print(f'user ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    print('BOT: ', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting...')
    app = Application.builder().token(TOKEN).build()

    #Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('status', status_command))
    
    #Conversation Handler
    convo_handler = ConversationHandler(
        entry_points = [CommandHandler('register', register_command)],
        states ={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            ID_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_id_number)]
        },
        fallbacks = [CommandHandler('regCancel', regCancel)]
    )
    app.add_handler(convo_handler)

    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Errors 
    app.add_error_handler(error)

    #Poll
    print('Polling...')
    app.run_polling(poll_interval = 7)
