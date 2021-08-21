import telebot
import cryptocompare
import time

info_message= "info here"
help_message = "help here"
start_message = "hey"
subbed_message = "subbed!"

#coins go here
coins=["BTC","BCH"]

#token
bot_token = ''

#creating neccesery obj
bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands = ['start'])
def send_welcome (message):
    global start_message
    bot.reply_to(message, start_message)

@bot.message_handler(commands = ['help'])
def send_help (message):
    global help_message
    bot.reply_to(message , help_message)

@bot.message_handler(commands = ['info'])
def send_info (message):
    global info_message
    bot.reply_to(message , info_message)

@bot.message_handler(commands = ['sub'])
def add_sub (message):
    subbed = False
    with open('subs_user_ids.txt','r') as f:
        while True:
            line = f.readline()
            if line==str(message.chat.id):
                subbed=True
            if not line:
                break
    if subbed:
        bot.reply_to(message,"You are already subbed !")
    else :
        with open('subs_user_ids.txt','a+') as f:
            f.write(str(message.chat.id))
        bot.reply_to(message , subbed_message)

@bot.message_handler(func=lambda msg: msg is not None and 'price' in msg.text)
def send_price (message):
    global not_ready_message , space_err_message
    coin_name = message.text.split()[1].upper()
    if coin_name in coins:
        price = cryptocompare.get_price(coin_name, 'USD')
        rep_txt =  "📈 "+ coin_name + " : " + str(price[coin_name]['USD']) + " USD"
        bot.reply_to(message,rep_txt)
    else :
        bot.reply_to(message,"This coin is not added yet!")

################################################

def notify():
    subs=[]
    with open('subs_user_ids.txt','r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            subs.append(line)
    notify_message =""
    for coin_name in coins:
        price = cryptocompare.get_price(coin_name, 'USD')
        rep_txt =  "📈 "+ coin_name + " : " + str(price[coin_name]['USD']) + " USD"
        notify_message += rep_txt+'\n'
    for sub in subs:
        bot.send_message(sub,notify_message)
#running
while True :
    try :
        notify()
        bot.polling()
    except Exception:
        time.sleep(15)