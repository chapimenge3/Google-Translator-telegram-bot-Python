'''My name is Chapi Menge.Am just Programmer'''
from googletrans import Translator
from googletrans import Translator
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,ConversationHandler)
import logging
from telegram import Bot
import telegram
'''for the admin notify the logger info'''
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO
                    )
logger = logging.getLogger(__name__)

translator = Translator()
token = 'Your token'
bot = Bot(token)
IN = range(1)
form = """
Send me word in any Language and Enter the text You want To Translate
after that add the word to and the language you want to Translate.
For Example - 
<strong>ፍቅር to English </strong>  or 
<strong>love to hindu </strong>
<strong>Life is just a chance to grow a soul to amharic</strong>
then send it to me"""

LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu',
    'fil': 'Filipino',
    'he': 'Hebrew'
}

LANGCODES = dict(map(reversed, LANGUAGES.items()))
def start(update,context):
    ''' opening conversation
    when you send /start to the bot
    you can change every string to your customized names or description 
    '''

    logger.info("Mr of %s: start conversations", update.message.from_user.first_name)
    context.bot.send_message(chat_id=update.message.chat_id, 
        text="Wellcome to Google Translation bot. Mr/Mrs "+ update.message.from_user.first_name+ " Chapi's Always Favorite and Bestie")
    update.message.reply_text(form,parse_mode=telegram.ParseMode.HTML)

    return IN  # return to state IN and wherever you enter or send it first find in IN
def translater(update,context):
    ''' Translator Function
    it takes string and split it 
    then check 
            1.the word 'to' in the text 
            2.the length of the splited text must greater than 2 means it must have at least one additional word other than 'to' and des.. language
            3.check the language the user entered is found on the language dictionary  
    it then take the last word as a destination language if it is valid 
    then delete it the last first means the destination language and last second means 'to'
    get the code for the destination language from getdest function
    the join the text by space to have the original text format and send to to the translator function
    finally print the text and pronunciation of the word 
    if the last 3 condition is false it sends error message to input the user again
    '''
    
    global text
    text = update.message.text
    dest = text.split()[-1]
    if 'to' in text and len(text.split()) > 2 and languagecheck (dest):
        text = text.split()
        dest = text[-1]
        dest = getdest(dest)
        del text[-2],text[-1]
        text = ' '.join(text)
        text = trans(text,dest)
        context.bot.send_message(chat_id=update.message.chat_id , text="""
Translation is 
_________________
<strong>{}</strong>
_________________
pronunciation is 
_________________
<strong>{}</strong>
""".format(text.text,text.pronunciation ),parse_mode=telegram.ParseMode.HTML )
        update.message.reply_text(form,parse_mode=telegram.ParseMode.HTML)
    else:
        update.message.reply_text('Please Enter in The correct format your input is invalid ')
        update.message.reply_text(form,parse_mode=telegram.ParseMode.HTML)
        # print(text.text)
    return IN
def trans(text,dest='en'):
    ''' Translator Function 
    it Translate the text to the destionation language'''
    return  translator.translate(text,dest=dest)
def cancel(update, context):
    ''' to cancel the conversation'''
    update.message.reply_text('Thank you! I hope we can talk again some day.\n')
    return ConversationHandler.END
def echo(update, context):
    ''' echo if any one cancel the conversation and send text to be translated'''
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please send /start to start conversation")
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
def languagecheck(text):
    if text.lower() in LANGCODES:
        return True
    else:
        return False
def getdest(dest="english"):
    try:
        return LANGCODES[dest.lower()]
    except:
        return False
def main():
    ''' updater startup'''
    updater = Updater(token=token,use_context=True)
    dispatcher = updater.dispatcher
    '''conversation  handeled by this''' 
    conv_handler = ConversationHandler (
        entry_points=[CommandHandler('start', start)],

        states={
            IN: [MessageHandler(Filters.text , translater)],
            
        },

        fallbacks=[CommandHandler('cancel', cancel)] ,)
    
    
    ''' registering the hander to dispatcher'''
    
    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_error_handler(error)
    dispatcher.add_handler(conv_handler)
    ''' start fetching dat from the telegram'''
    updater.start_polling()
    ''' to stop the code runnig in the cmd by control+c'''
    updater.idle()

'''driver'''
if __name__ == '__main__':
    main()
