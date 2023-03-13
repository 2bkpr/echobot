import json
import requests
import urllib
import bot_config
# def send_document(doc, chat_id):
#     files = {'document': open(doc, 'rb')}
#     requests.post(URL + "sendDocument?chat_id={}".format(chat_id), files=files)
#
#
# def send_image(doc, chat_id):
#     files = {'photo': open(doc, 'rb')}
#     requests.post(URL + "sendPhoto?chat_id={}".format(chat_id), files=files)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = bot_config.URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    for update in updates["result"]:
        if update.get("message") != None:
            if update.get("message", {}).get("text") != None:
                text = update["message"]["text"]
                chat = update["message"]["chat"]["id"]
                print(text)
                # if text == "/test" or text == "/test@" + bot_config.USERNAME_BOT:
                #     text = "test response"
                #     send_message(text, chat)
                # elif text == "/start" or text == "/start@" + bot_config.USERNAME_BOT:
                #     send_message("/test for test the bot", chat)
                if text == "/start" or text == "/start@" + bot_config.USERNAME_BOT:
                    bot_message = "Hello, I'm echo bot. Can you be nigger for me ?"
                    send_message(bot_message, chat)
                else:
                    bot_message = text
                    send_message(bot_message, chat)


def send_message(text, chat_id):
    tot = urllib.parse.quote_plus(text)
    url = bot_config.URL + "sendMessage?text={}&chat_id={}".format(tot, chat_id)
    get_url(url)


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        print(updates)
        if updates is not None:
            if len(updates["result"]) > 0:
                last_update_id = get_last_update_id(updates) + 1

                echo_all(updates)

if __name__ == '__main__':
    main()