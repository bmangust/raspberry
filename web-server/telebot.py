import datetime
import telepot
from telepot.loop import MessageLoop
import RPi.GPIO as G
from time import sleep

led1 = 14
led2 = 13

G.setmode(G.BCM)
G.setup(led1, G.OUT)
G.setup(led2, G.OUT)

new = datetime.datetime.now()

def handle(msg):
    chat_id = msg['chat']['id'] # Receiving the message from telegram
    command = msg['text']   # Getting text from the message

    print ('Received:')
    print(command)

    # Comparing the incoming message to send a reply according to it
    if command == '/hi':
        bot.sendMessage (chat_id, str("Hi! MakerPro"))
    elif command == '/time':
        bot.sendMessage(chat_id, str("Time: ") + str(now.hour) + str(":") + str(now.minute) + str(":") + str(now.second))
    elif command == '/date':
        bot.sendMessage(chat_id, str("Date: ") + str(now.day) + str("/") + str(now.month) + str("/") + str(now.year))
    elif command == '/blue_1':
        bot.sendMessage(chat_id, str("Blue led is ON"))
        G.output(led1, G.HIGH)
    elif command == '/orange_1':
        bot.sendMessage(chat_id, str("Orange led is ON"))
        G.output(led2, G.HIGH)
    elif command == '/blue_0':
        bot.sendMessage(chat_id, str("Blue led is OFF"))
        G.output(led1, G.LOW)
    elif command == '/orange0':
        bot.sendMessage(chat_id, str("Orange led is OFF"))
        G.output(led2, G.LOW)

bot = telepot.Bot('1087035980:AAF5slWHqtHRA61a3GMLcV30Z1Kmheh3Pa0')
print (bot.getMe())

MessageLoop(bot, handle).run_as_thread()
print('Listening...')

while 1:
    sleep(10)
