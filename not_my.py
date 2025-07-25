import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import datetime as dt


mat = ['', '', '', '', '', '', '', '', '']
hi = ['хэй', 'привет', "здравствуйте", "ку", 'рад видеть вас', 'доброго времени суток']
good = ['добрый день', 'добрый вечер', 'доброе утро', 'доброй ночи']
token = "c178ebd1413fa754e95a61b37d2d121284b65fc8317679ef56fb0ada11e1a059805631648c032bdcb943e"
vk = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk, 213287994)


def sender(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message})


for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.from_chat:

            id = event.chat_id
            msg = event.object.message['text'].lower()

            if msg.capitalize() in good:
                b = int(dt.datetime.now().strftime("%H")) - 2
                if 5 >= b >= 23:
                    sender(id, "Доброй ночи")
                elif 12 >= b >= 7:
                    sender(id, "Доброе утро")
                elif 12 < b <= 18:
                    sender(id, "Добрый день")
                elif 18 < b < 23:
                    sender(id, "Добрый вечер")
            elif msg in hi:
                a = random.randint(0, 5)
                sender(id, hi[a].capitalize())
            elif 'справка' == msg:
                sender(id, 'Могу здороваться с вами')

