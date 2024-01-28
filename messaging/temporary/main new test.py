from typing import Final
import telegram
from telegram import Update, constants, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import asyncio

TOKEN: Final = '6773869793:AAFx4-e23HUBsaY9bFBD5IeoJQsSf_fXSSs'
BOT_USERNAME: Final = '@BCHTEST2Bot'
NAME, ID_NUMBER = range(2)
AGE, MEDICALLY_OBESE, VACCINATED, ASE_LEVEL, IMMUNITY_SUPP, HEALTHY_SLEEP_CYCLE, ANTIBODIES, DIABETIC, HTRY_HEART = range(9)
USER_INFO_FILE_PATH = '/Users/hearth/BCHACKS_5.0/Ramses/eunaiBot/reg_result.txt' #extracting user info 

#Arrays
commands = [
    ('/start', 'Intializes the bot'), ('/help', 'Lists all known commands'), ('/status', 'Provides your current health status'), 
    ('/register', 'Intiates registration process'), ('/regCancel', 'Cancels the registration process'), ('/examination', 'Begins your risk assesment'),
    ('examCancel', 'Terminates the examination process')

]
user_data_array = [] #stores name and id, currently UNUSED
user_info_array = [] #stores data for back-end

#Misc functions, formatting etc
def format_help_command(commands):
    return '\n'.join([f'{command}: {description}' for command, description in commands])

def user_info_to_file(file_path, user_info):
    with open(file_path,'w') as file:
        for data in user_info:
            for key, value in data.items():
                file.write(f'{value} ')
                
#Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello!, I am Eunai. How can I help you today?\n')
    await update.message.reply_text('Please use the /register command to link Eunai with your data if you are a new user!')
    await update.message.reply_text('Type /help for a list of commands.')
    
    chat_id = update.message.chat_id
    userChatsFile = open('userchats.txt', 'a')
    userChatsFile.write(str(chat_id)+"\n")
    userChatsFile.close()

    userChatsFile = open('userchats.txt', 'r')
    print(userChatsFile.readline()  )
    userChatsFile.close()

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands_list = format_help_command(commands)
    help_message = ('Here is what I can do:')
    await update.message.reply_text(help_message)
    await update.message.reply_text(commands_list)

####################
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Custom Command')
####################



async def announce_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    announcement = ('[Alert] You may be at risk of illness!')
    with open('userchats.txt', 'r') as userChatsFile:
        for line in userChatsFile:
            print(line)
            await context.bot.send_message(chat_id=line, text=announcement)
       
async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Yes", callback_data="1"),
            InlineKeyboardButton("No", callback_data="2")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Would you like to self report illness?", reply_markup=reply_markup)


async def report_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if query.data=="2":
        await query.edit_message_text(text="Report cancelled.")
    else:
        await query.edit_message_text(text="You have self reported as sick. Please seek medical assistance or a SMART Test Kit to verify your report immediately.")
        announcement = ('An illness report [UNVERIFIED] has been made by someone you may have been in contact with!')
        with open('userchats.txt', 'r') as userChatsFile:
            for line in userChatsFile:
                print(line)
                await context.bot.send_message(chat_id=line, text=announcement)



async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    intro = ('Please wait while I pull your data')
    await update.message.reply_text(intro)
    await context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.constants.ChatAction.TYPING)
    await asyncio.sleep(3)
    #TODO
    
#Registration command, and linking with convo handler
async def register_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Beginning registration process!')
    await context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.constants.ChatAction.TYPING)
    await asyncio.sleep(3)
    await update.message.reply_text('IMPORTANT: Please use the /regCancel command to terminate ongoing registration process')
    await update.message.reply_text('....\n....\n.....\n......')
    await update.message.reply_text('Please tell me your first name.')
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.text
    context.user_data['name'] = user_name
    await update.message.reply_text(f'Thank you {user_name}. Please tell me your ID NUMBER assigned by the Space Health Ministry.')
    return ID_NUMBER

async def get_id_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.text
    context.user_data['id_number'] = user_id
    completion_msg = f'Registration is now complete.\nVerify your information. If you need to make changes, re-initiate the registration process.' 
    userId_msg = f'\n Username: {context.user_data["name"]}\nID_Number: {user_id}'
    user_name = context.user_data.get('name', 'not provided')
    user_data_array.append({'Name': user_name}, {'ID_Number': user_id}) #stores username and id into user_data array
    await update.message.reply_text(completion_msg)
    await update.message.reply_text(userId_msg)
    return ConversationHandler.END

async def regCancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Registration has been cancelled...\nComplete registration to continue using Eunai.')
    return ConversationHandler.END #ends convo

async def examination_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('We will begin your initial analysis now.') #actual bullshit
    await update.message.reply_text('IMPORTANT: Please use the /examCancel command to terminate analysis.')
    #await update.message.reply_text('\nAs per section 296 of the Space Station Criminal Code, individuals must answer truthfully.')
    #await update.message.reply_text('\nIndividuals found with fraudulent data will be prosecuted and subject to interrogation and excecution')
    #await update.message.reply_text('\nUphold your integrity. May the stars bless you, we are watching')

    await update.message.reply_text('Please tell me your age.')
    return AGE

async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_age = (update.message.text)
    if user_age.isdigit():
        user_age = int(user_age)
        if user_age > 0:
            is_over_65 = 1 if user_age > 65 else 0
            is_under_5 = 1 if user_age < 5 else 0
            user_info_to_file(USER_INFO_FILE_PATH, user_info_array)
            age_temp = {
                'age' : user_age, 'is_over_65': is_over_65, 'is_under_5' : is_under_5
            }
            user_info_array.append(age_temp)
            await update.message.reply_text('Response recorded.')
            user_info_to_file(USER_INFO_FILE_PATH, user_info_array)
            await context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.constants.ChatAction.TYPING)
            await asyncio.sleep(3)
            await update.message.reply_text('Are you medically obese?\n 1 for Yes, 0 for No')

            return MEDICALLY_OBESE
    else:
        await update.message.reply_text('Invalid input. Please re-enter a valid age.')
        return AGE

async def get_obese(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_obese = update.message.text
    if user_obese == '1' or user_obese == '0':
        context.user_data['medically_obese'] = int(user_obese)
        user_info_array.append({'medically_obese': int(user_obese)})
        await update.message.reply_text('Response recorded.')
        user_info_to_file(USER_INFO_FILE_PATH, user_info_array)
        await asyncio.sleep(3)
        await update.message.reply_text('Are you vaccinated?\n 1 for Yes, 0 for No')
        return VACCINATED
    else:
        await update.message.reply_text('Re-enter a valid answer.')
        return MEDICALLY_OBESE

async def get_vaccinated(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_vacc = update.message.text
    if user_vacc == '1' or user_vacc == '0':
        context.user_data['vaccinated'] = int(user_vacc)
        user_info_array.append({'vaccinated': user_vacc})
        await update.message.reply_text('Response recorded.')
        user_info_to_file(USER_INFO_FILE_PATH, user_info_array)
        await asyncio.sleep(3)
        await update.message.reply_text('What are your Artificial Sun Exposure Levels? (0-100): ')
        return ASE_LEVEL
    else:
        await update.message.reply_text('Re-enter a valid answer.')
        return VACCINATED
    
async def get_ASE(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_ASE = update.message.text
    user_ASE = int(user_ASE)
    if user_ASE < 0 or user_ASE > 100:
        await update.message.reply_text('Re-enter a number between 0 and 100.')
        return ASE_LEVEL
    else:
        context.user_data['ASE_Level'] = user_ASE
        user_info_array.append({'ASE level': user_ASE})
        await update.message.reply_text('Response recorded.')
        user_info_to_file(USER_INFO_FILE_PATH, user_info_array)
        await asyncio.sleep(3)
        await update.message.reply_text('Do you take immunity supplements?\n 1 for Yes, 0 for No')
        return IMMUNITY_SUPP
    
async def get_immunity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_immunity = update.message.text
    if user_immunity == '1' or user_immunity == '0':
        context.user_data['immunity'] = int(user_immunity)
        user_info_array.append({'immunity': user_immunity})
        await update.message.reply_text('Response recorded.')
        user_info_to_file(USER_INFO_FILE_PATH, user_info_array)
        await asyncio.sleep(3)
        await update.message.reply_text('Do you have a healthy sleep schedule\n 1 for Yes, 0 for No')

        return HEALTHY_SLEEP_CYCLE
    else:
        await update.message.reply_text('Re-enter a valid answer.')
        return IMMUNITY_SUPP
    
async def get_sleep_cycle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_sleep = update.message.text
    if user_sleep == '1' or user_sleep == '0':
        context.user_data['healthy_sleep_cycle'] = int(user_sleep)
        user_info_array.append({'healthy_sleep_cycle': user_sleep})
        await update.message.reply_text('Response recorded.')
        user_info_to_file(USER_INFO_FILE_PATH, user_info_array)
        await asyncio.sleep(3)
        await update.message.reply_text('Have you been sick recently?\n 1 for Yes, 0 for No')
        return ANTIBODIES
    else:
        await update.message.reply_text('Re-enter a valid answer.')
        return HEALTHY_SLEEP_CYCLE

async def get_antibodies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_antibodies = update.message.text
    if user_antibodies == '1' or user_antibodies == '0':
        context.user_data['antibodies'] = int(user_antibodies)
        user_info_array.append({'antibodies': user_antibodies})
        await update.message.reply_text('Response recorded.')
        user_info_to_file(USER_INFO_FILE_PATH, user_info_array)
        await asyncio.sleep(3)
        await update.message.reply_text('Are you diabetic?\n 1 for Yes, 0 for No')
        return DIABETIC
    else:
        await update.message.reply_text('Re-enter a valid answer.')
        return ANTIBODIES

async def get_diabetic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_diabetic = update.message.text
    if user_diabetic == '1' or user_diabetic == '0':
        context.user_data['diabetic'] = int(user_diabetic)
        user_info_array.append({'diabetic': user_diabetic})
        await update.message.reply_text('Response recorded.')
        user_info_to_file(USER_INFO_FILE_PATH, user_info_array)
        await asyncio.sleep(3)
        await update.message.reply_text('Do you have a history of heart disease\n 1 for Yes, 0 for No')
        return HTRY_HEART
    else:
        await update.message.reply_text('Re-enter a valid answer.')
        return DIABETIC
    
async def get_heart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_heart = update.message.text
    if user_heart == '1' or user_heart == '0':
        context.user_data['heart_disease'] = int(user_heart)
        user_info_array.append({'heart_disease': user_heart})
        await update.message.reply_text('Response recorded.')
        user_info_to_file(USER_INFO_FILE_PATH, user_info_array)
        await asyncio.sleep(3)
        await update.message.reply_text('Your examination is now complete. Congratulations!')
        return ConversationHandler.END
    else:
        await update.message.reply_text('Re-enter a valid answer.')
        return HTRY_HEART

async def exam_cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Your analysis has been cancelled, please use the /examination command to perform the analysis again.')
    return ConversationHandler.END

#Responses 
def handle_response(text: str) -> str:
    processed: str = text.lower()
    if 'hello' in processed:
        return 'Hello!'
    if 'help' in processed:
        return 'Please use the /help command.'
    
    return 'I am not quite sure what you are saying, please use the provided commands.'


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
    app.add_handler(CommandHandler('announce', announce_command))
    app.add_handler(CommandHandler('report', report_command))
    app.add_handler(CallbackQueryHandler(report_choice))
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
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
            MEDICALLY_OBESE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_obese)],
            VACCINATED: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_vaccinated)],
            ASE_LEVEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_ASE)],
            IMMUNITY_SUPP: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_immunity)],
            HEALTHY_SLEEP_CYCLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_sleep_cycle)],
            ANTIBODIES: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_antibodies)],
            DIABETIC: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_diabetic)],
            HTRY_HEART: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_heart)],
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
    app.run_polling(poll_interval = 2)
