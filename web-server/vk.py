# -*- coding: utf-8 -*-i
import datetime
import time
import vk_api
from socket import gethostbyname
from vk_api.utils import get_random_id
import RPi.GPIO as G


led1 = 14
led2 = 13

G.setmode(G.BCM)
G.setup(led1, G.OUT)
G.setup(led2, G.OUT)

now = datetime.datetime.now()  

vk = vk_api.VkApi(token = 'YOUR_TOKEN')
 
param = {
    'count': 1,
    'time_offset': 5,
    'filter': 'unread'
}
 
 
def write_msg(user_id, msg): 
    vk.method('messages.send', { 
        'user_id': user_id, 
        'message': msg,
        'random_id':get_random_id()
    })


def execute(user_id, command):
        if command == '/Hi':
            write_msg (user_id, str("Hi! MakerPro"))
        elif command == '/Time':
            write_msg(user_id, str("Time: ") + str(now.hour) + str(":") + str(now.minute) + str(":") + str(now.second))
        elif command == '/Date':
            write_msg(user_id, str("Date: ") + str(now.day) + str("/") + str(now.month) + str("/") + str(now.year))
        elif command == '/Blue_1':
            write_msg(user_id, str("Blue led is ON"))
            G.output(led1, G.HIGH)
        elif command == '/Orange_1':
            write_msg(user_id, str("Orange led is ON"))
            G.output(led2, G.HIGH)
        elif command == '/Blue_0':
            write_msg(user_id, str("Blue led is OFF"))
            G.output(led1, G.LOW)
        elif command == '/Orange_0':
            write_msg(user_id, str("Orange led is OFF"))
            G.output(led2, G.LOW)
        elif command == '/Getip':
            IPAddr = gethostbyname('124raspberry')
            write_msg(user_id, IPAddr)
        elif command.startswith('/'):
            write_msg(user_id, 'unknown command: ' + command)
        else:
            write_msg(user_id, command)
 
 
try:
    while True: 
        response = vk.method('messages.getConversations', param) 
        if response['items']:
#            print(response)
            item = response['items'][0] 
            last_mess = item['last_message'] 
            my_id = last_mess['peer_id'] 
            text = last_mess['text']
            execute(my_id, text)
        time.sleep(1) 
except KeyboardInterrupt:
    print('Keyboard interrupt detected.')
finally:
    print('The program was stopped.')
    G.cleanup()
