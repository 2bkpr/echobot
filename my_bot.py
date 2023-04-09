import requests
import bot_config
import json
import time
import urllib
from dbhelper import DBHelper
import os
import pprint

db = DBHelper()


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


def echo_all(updates, products_data, current_product): #(updates, states_list, current_state)
    #pprint.pprint(updates)
    if 'text' in updates['result'][0]['message']:
        for update in updates["result"]:
            try:
                text = update["message"]["text"]
                chat = update["message"]["chat"]["id"]
                total_products = len(products_data)
                # if text in states_list:
                #     current_state = text
                # send_message(current_state, chat)
                # return current_state
                if text == "/start":
                    text = "Hello, I'm a market bot.\nInput /show_menu to watching next or previous products"
                    send_message(text, chat)
                    send_next_product(chat, products_data[0])
                    print("Вызов из echo_all", current_product % total_products)
                elif text == "/show_menu":
                    text = "Select the button"
                    keyboard = build_keyboard()
                    send_message(text, chat, keyboard)
                elif text == "/help":
                    text = "ДОБАВИТЬ ТЕКСТ"
                    send_message(text, chat)
                elif text == "Next item":
                    current_product += 1
                    print("Вызов из echo_all", current_product % total_products)
                    send_next_product(chat, products_data[current_product % total_products])
                elif text == "Previous item":
                    current_product -= 1
                    print("Вызов из echo_all", current_product % total_products)
                    send_next_product(chat, products_data[current_product % total_products])
                return current_product
                # elif text == "/stop":
                #     pass
            except Exception as e:
                print(e)
    # elif 'photo' in updates['result'][0]['message']:
    #     for update in updates["result"]:
    #         try:
    #             chat = update["message"]["chat"]["id"]
    #             send_image(updates, chat)
    #         except Exception as e:
    #             print(e)


# def handle_updates(updates):
#     for update in updates["result"]:
#         try:
#             text = update["message"]["text"]
#             chat = update["message"]["chat"]["id"]
#             items = db.get_items()
#             if text in items:
#                 db.delete_item(text)
#                 items = db.get_items()
#             else:
#                 db.add_item(text)
#                 items = db.get_items()
#             message = "\n".join(items)
#             send_message(message, chat)
#         except KeyError:
#             pass


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
    keyboard = [["Next item"], ["Previous item"]]
    reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def get_data(product_data):
    product_info = product_data[1] + "\n" + product_data[2] + "\n" + "Coast: " + str(product_data[3])
    image_blob = product_data[4]
    with open('temp.jpg', 'wb') as file:
        file.write(image_blob)
    files = {'photo': open('temp.jpg', 'rb')}
    return product_info, files


def send_next_product(chat_id, product_data):
    product_info, files = get_data(product_data)
    data = {
        'chat_id': chat_id,
        'caption': product_info,
        'parse_mode': 'MarkdownV2',
    }
    requests.post(f"https://api.telegram.org/bot{bot_config.TOKEN}/sendPhoto", data=data, files=files)
    #os.remove('temp.jpg')


def main():
    db.setup()
    last_update_id = None
    products_data = db.get_items()
    current_product = 0
    #states_list = ["morning", "day", "evening", "night"]
    #current_state = states_list[0]
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            current_product = echo_all(updates, products_data, current_product)
            print("Вызов из main", current_product)
            # handle_updates(updates)
            #current_state = echo_all(updates, states_list, current_state)

        time.sleep(0.5)


if __name__ == '__main__':
    main()