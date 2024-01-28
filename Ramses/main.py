from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

TOKEN: Final = '6818698464:AAExduA8qUwEWa3wl1i_M2gK3OVF2Uv0-Fk'
BOT_USERNAME: Final = '@EunaiBot'
NAME, ID_NUMBER = range(2)
#Arrays
commands = [
    ('/start', 'Intializes the bot'), ('/help', 'Lists all known commands'), ('/status', 'Provides your current health status'), 
    ('/register', 'Intiates registration process'), ('/regCancel', 'Cancels the registration process'), ('/examination', 'Begins your risk assesment')

]
user_data_array = [] #stores name and id, currently UNUSED
user_info_array = [] #stores data for back-end

#Misc functions, formatting etc
def format_help_command(commands):
    return '\n'.join([f'{command}: {description}' for command, description in commands])

def to_text_file(user_data): #stores data into txt file then backend prediction
    with open('user_info.txt', 'w') as file:
        for user_data in user_data_array:
            file.write 
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
    await update.message.reply_text('....\n....\n.....\n......')
    await update.message.reply_text('Enter your full legal name:')
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
    user_name = context.user_data.get('name', 'not provided')
    user_data_array.append({'Name': user_name}, {'ID_Number': user_id}) #stores username and id into user_data array

    await update.message.reply_text(completion_msg)
    await update.message.reply_text(userId_msg)
    return ConversationHandler.END

async def regCancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Registration has been cancelled...\nComplete registration to continue using Eunai')
    return ConversationHandler.END #ends convo

async def examination_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('We will begin your analysis now.') #actual bullshit
    await update.message.reply_text('\nAs per section 296 of the Space Station Criminal Code. Individuals must answer truthfully')
    await update.message.reply_text('\nIndividuals found with fraudulent data will be prosecuted and subject to interrogation and excecution')
    await update.message.reply_text('\nUphold your integrity. May the stars bless you, we are watching')
    return AGE

async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Please enter your age')
    user_age = (update.message.text)
    if user_age.isdigit():
        if user_age > 0:
            is_over_65 = 1 if user_age > 65 else 0
            is_under_5 = 1 if user_age < 5 else 0
            age_temp = {
                'age' : user_age, 'is_over_65': is_over_65, 'is_under_5' : is_under_5
            }
            user_data_array.append(age_temp)
            await update.message.reply_text('Thank you, lets proceed.')
            return MEDICALLY_OBESE
    else:
        await update.message.reply_text('Invalid input. Please enter a valid age')
        return AGE

async def get_obese(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Are you medically obese?\n 1 for Yes, 0 for No')
    user_usa = update.message.text
    if user_usa == '1' or user_usa == '0':
        context.user_data['obese'] = int(user_usa)
        await update.message.text_reply(f'Medically Obese: {user_usa} - Recorded')

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
    #questions for back-end processing 
    #has to return reg_result.txt
    information_handler = ConversationHandler(
        entry_points = [CommandHandler('examination', examination_command)],
        states ={
            AGE:
            MEDICALLY_OBESE:
            VACCINATED:
            ASE_LEVEL:
            IMMUNITY_SUPP:
            HEALTHY_SLEEP_CYCLE:
            ANTIBODIES:
            DIABETIC:
            HTRY_HEART:
        },
        fallbacks = [CommandHandler('examCancel', exam_cancel_command)]
    )
    app.add_handler(information_handler)

    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Errors 
    app.add_error_handler(error)

    #Poll
    print('Polling...')
    app.run_polling(poll_interval = 7)
