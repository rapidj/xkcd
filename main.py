import requests
import os
from dotenv import load_dotenv
from pathlib import Path
import random
import logging
import telegram
import telegram.error as tg_error


def fetch_last_comic_num():
    current_comic_url = 'https://xkcd.com/info.0.json'
    xkcd_response = requests.get(current_comic_url)
    xkcd_response.raise_for_status()
    last_comic_num = xkcd_response.json()['num']
    return last_comic_num


def download_image(url, file_name, dir_name, extension='.png', params=None):
    full_file_name = f'{file_name}{extension}'
    file_path = os.path.join(dir_name, full_file_name)
    response = requests.get(url, params=params)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)


def download_comic(comic_number, dir_name):
    comic_url = f'https://xkcd.com/{comic_number}/info.0.json'
    comic_response = requests.get(comic_url)
    comic_response.raise_for_status()
    comic_details = comic_response.json()
    comic_comments = comic_details['alt']
    comic_image_url = comic_details['img']
    comic_image_name = f'comic_{comic_number}'
    download_image(comic_image_url, comic_image_name, dir_name)
    return comic_comments


def fetch_images_list(path):
    paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            paths.append(os.path.join(root, file))
    return paths


def send_image(bot, chat_id, image, comic_comments):
    with open(image, 'rb') as image_to_send:
        bot.send_photo(chat_id=chat_id, photo=image_to_send, caption=comic_comments)


def main():
    load_dotenv()
    tlg_token = os.environ['TLG_BOT_TOKEN']
    tlg_chat_id = os.environ['TLG_CHANNEL_ID']
    bot = telegram.Bot(token=tlg_token)

    dir_name = 'images'
    Path(dir_name).mkdir(parents=True, exist_ok=True)

    last_comic_num = fetch_last_comic_num()
    random_comic_num = random.randint(1, last_comic_num)
    comic_comments = download_comic(random_comic_num, dir_name)

    images = fetch_images_list('images')
    if not images:
        logging.error("No images in the '.images' folder")
        return

    try:
        if images[0]:
            send_image(bot, tlg_chat_id, images[0], comic_comments)
    except tg_error.NetworkError as e:
        logging.info('Problems with internet connection')

    finally:
        for image in images:
            os.remove(image)


if __name__ == '__main__':
    main()
