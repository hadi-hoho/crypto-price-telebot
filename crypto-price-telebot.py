import telebot, cryptocompare, time, threading

info_message = "This bot can send you real-time prices of crypto currencies\nAlso will notify in certain times which can be modified by the Admin \nThis bot is using a open-source code \n   you can access this code in https://github.com/hadi-hoho/crypto-price-telebot"
help_message = 'usage :\n /help - get this message\n /info - get info message\n /sub - subscribe to the notification option\nGet a coin price by :\n      "price [coin]"\n      e.g.:"price btc"'
start_message = "Hello there! \n use /help"
subbed_message = "subbed!"
notif_time = 360  # in minute

# coins go here
coins = ["BTC", "BCH", "ETH", "USDT", "XRP", "DOGE", "LTC", "ETC", "XMR"]

# getting the token
try:
    with open("bot_token", "r") as token_file:
        bot_token = token_file.read()
except Exception as err_inst:
    print("something went wrong while getting the bot token")
    raise Exception("unable to get token") from err_inst

# creating bot obj
bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    global start_message
    bot.reply_to(message, start_message)


@bot.message_handler(commands=["help"])
def send_help(message):
    global help_message
    bot.reply_to(message, help_message)


@bot.message_handler(commands=["info"])
def send_info(message):
    global info_message
    bot.reply_to(message, info_message)


@bot.message_handler(commands=["sub"])
def add_sub(message):
    subbed = False
    with open("subs_user_ids.txt", "r") as f:
        lines = f.readlines()
        if str(message.chat.id) + "\n" in lines:
            subbed = True
        print(lines)
    if subbed:
        bot.reply_to(message, "You are already subbed !")
    else:
        with open("subs_user_ids.txt", "a") as f:
            f.write(str(message.chat.id) + "\n")
        bot.reply_to(message, subbed_message)


@bot.message_handler(func=lambda msg: msg is not None and "price" in msg.text)
def send_price(message):
    global not_ready_message, space_err_message
    coin_name = message.text.split()[1].upper()
    if coin_name in coins:
        price = cryptocompare.get_price(coin_name, "USD")
        rep_txt = "📈 " + coin_name + " : " + str(price[coin_name]["USD"]) + " USD"
        bot.reply_to(message, rep_txt)
    else:
        bot.reply_to(message, "This coin is not added yet!")


################################################


def notify():
    subs = []
    with open("subs_user_ids.txt", "r") as f:
        while True:
            line = f.readline()
            if not line:
                break
            subs.append(line)
    notify_message = ""
    for coin_name in coins:
        price = cryptocompare.get_price(coin_name, "USD")
        rep_txt = "📈 " + coin_name + " : " + str(price[coin_name]["USD"]) + " USD"
        notify_message += rep_txt + "\n\n"
    for sub in subs:
        try:
            bot.send_message(sub, notify_message)
        except:
            pass


def notifier():
    while True:
        notify()
        time.sleep(notif_time * 60)


# running

# Starting a Thread For Notify
thread = threading.Thread(target=notifier, args=())
thread.start()

while True:
    try:
        bot.polling()
    except Exception:
        print("### someting went wrong")
        time.sleep(15)
