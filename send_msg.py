import telepot

def telegram_bot(bot_message):
    token = '5191783581:AAHFHW05uc0TafGo-qenjmrHMn51nP-rLdg' # telegram token
    receiver_id = 990932798 # https://api.telegram.org/bot<TOKEN>/getUpdates


    bot = telepot.Bot(token)

    bot.sendMessage(receiver_id, bot_message) # send a activation message to telegram receiver id





