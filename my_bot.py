import requests
import bot_config
import json
import time
import urllib
import pprint


def get_url(url): # получение json формата
    response = requests.get(url)
    content = response.content#.decode("utf8")
    return content


def get_json_from_url(url): # Десереализация json формата полученного от запроса
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None): # Получение всей инф о чате от которого пришло сообщение
    url = bot_config.URL + "getUpdates?timeout=100"
    if offset:
        url += f"&offset={offset}"
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates, states_list, current_state):
    #pprint.pprint(updates)
    if 'text' in updates['result'][0]['message']:
        for update in updates["result"]:
            try:
                text = update["message"]["text"]
                chat = update["message"]["chat"]["id"]
                if text in states_list:
                    current_state = text
                send_message(current_state, chat)
                return current_state
                # if text == "/start":
                #     text = "Hello, I'm echo bot."
                #     send_message(text, chat)
                # elif text == "/show_button":
                #     text = "Select the button"
                #     keyboard = build_keyboard()
                #     send_message(text, chat, keyboard)
                # else:
                #     send_message(text, chat)
            except Exception as e:
                print(e)
    elif 'photo' in updates['result'][0]['message']:
        for update in updates["result"]:
            try:
                #text = "Photo"
                chat = update["message"]["chat"]["id"]
                #send_message(text, chat)
                send_image(updates, chat)
            except Exception as e:
                print(e)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return text, chat_id


def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = bot_config.URL + f"sendMessage?text={text}&chat_id={chat_id}"
    if reply_markup:
        url += f"&reply_markup={reply_markup}"
    get_url(url)


def get_image(update):
    img_id = update['result'][0]['message']['photo'][-1]["file_id"]
    url = bot_config.URL + f"getFile?file_id={img_id}"
    image_info = get_json_from_url(url)
    path_image = image_info["result"]["file_path"]
    url = "https://api.telegram.org/file/bot5472404391:AAFzRL2xXLdvCDHL77kb__RffZ7yyMKTYCQ/" + path_image
    image_bytes = get_url(url)
    doc_path = "./res.jpg"
    with open(doc_path, "wb") as f:
        f.write(image_bytes)
    return doc_path


def send_image(update, chat_id):
    img_path = get_image(update)
    image = {'photo': open(img_path, 'rb')}
    requests.post(bot_config.URL + f"sendPhoto?chat_id={chat_id}", files=image)


def build_keyboard():
    keyboard = [["Show text"], ["One more text"]]
    reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)




def main():
    last_update_id = None
    states_list = ["morning", "day", "evening", "night"]
    current_state = states_list[0]
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            current_state = echo_all(updates, states_list, current_state)

        time.sleep(0.5)


if __name__ == '__main__':
    main()